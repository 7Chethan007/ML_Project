"""
Unified processing pipeline for many company JSONs:
- reads JSON files
- normalizes & cleans sections (cashflow, balancesheet, profitandloss)
- extracts 'analysis' section
- feature engineering (margins, leverage, growths, CAGR)
- caching/incremental behavior
- stores master CSV files + SQLite DB for quick queries
"""

import os
import glob
import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np
import sqlite3
from tqdm import tqdm
import warnings

# CONFIG
data_dir = os.path.join('..', 'data')   # adjust as needed
file_glob = os.path.join(data_dir, '*.json')
process_limit = None   # set to 5 for testing, or None for all
output_dir = './compiled_output'
os.makedirs(output_dir, exist_ok=True)

# Output filenames
csv_cashflow = os.path.join(output_dir, 'cashflow_master.csv')
csv_balancesheet = os.path.join(output_dir, 'balancesheet_master.csv')
csv_profitloss = os.path.join(output_dir, 'profitloss_master.csv')
csv_analysis = os.path.join(output_dir, 'analysis_master.csv')
csv_meta = os.path.join(output_dir, 'companies_meta.csv')
sqlite_db = os.path.join(output_dir, 'financials.db')

# --- HELPERS ---
def to_num(x):
    """Robust numeric conversion: remove commas, %; convert to float or NaN."""
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    if s in ['', '-', 'None', 'null', 'nan', 'NA']:
        return np.nan
    s = s.replace(',', '')
    # capture parentheses as negative e.g. (123)
    if re.match(r'^\(.*\)$', s):
        s = '-' + s[1:-1]
    # strip percent but keep numeric
    s = s.replace('%', '')
    try:
        return float(s)
    except:
        return np.nan

def parse_year_to_dt(y):
    """Keep 'TTM' flagged, parse 'Mar 2024' -> datetime (end of month).
       Returns (dt_or_NaT, is_ttm_flag, original_str)
    """
    if pd.isna(y):
        return (pd.NaT, False, y)
    if isinstance(y, (pd.Timestamp, datetime)):
        return (pd.to_datetime(y), False, str(y))
    s = str(y).strip()
    if s.upper() == 'TTM':
        return (pd.NaT, True, 'TTM')
    # Try formats like 'Mar 2024', 'Mar-2024', '2024-03-31'
    for fmt in ("%b %Y", "%b %Y", "%Y-%m-%d", "%Y"):
        try:
            dt = pd.to_datetime(datetime.strptime(s, fmt))
            return (dt, False, s)
        except:
            pass
    # fallback: try pandas parse
    try:
        dt = pd.to_datetime(s, errors='coerce')
        if pd.isna(dt):
            return (pd.NaT, False, s)
        return (dt, False, s)
    except:
        return (pd.NaT, False, s)

def compute_group_growth(df, company_col='company_id', value_col='sales', year_dt_col='year_dt'):
    """Compute YoY pct_change and simple CAGR between first and last available rows per company."""
    df = df.copy().sort_values([company_col, year_dt_col])
    df['{}_yoy'.format(value_col)] = df.groupby(company_col)[value_col].pct_change()
    # compute CAGR for group if possible
    def cagr(group):
        vals = group[value_col].dropna()
        if len(vals) < 2:
            return np.nan
        first, last = vals.iloc[0], vals.iloc[-1]
        n = len(vals) - 1
        if first <= 0 or n <= 0:
            return np.nan
        return (last / first) ** (1.0 / n) - 1.0
    cagr_df = df.groupby(company_col).apply(lambda g: pd.Series({'{}_cagr'.format(value_col): cagr(g)})).reset_index()
    return df, cagr_df

# --- FILE PROCESSING ---
def process_json_file(path):
    """Return dicts of dataframes for sections and metadata."""
    with open(path, 'r', encoding='utf-8') as f:
        j = json.load(f)
    cid = j.get('company', {}).get('id', Path(path).stem)
    company_meta = j.get('company', {})
    
    # ----- CASHFLOW
    cashflow = pd.DataFrame(j.get('data', {}).get('cashflow', []))
    if not cashflow.empty:
        cashflow['company_id'] = cid
        cashflow['year_orig'] = cashflow['year']
        parsed = cashflow['year_orig'].apply(parse_year_to_dt)
        cashflow['year_dt'] = [p[0] for p in parsed]
        cashflow['is_ttm'] = [p[1] for p in parsed]
        # numeric columns
        for col in ['operating_activity', 'investing_activity', 'financing_activity', 'net_cash_flow']:
            if col in cashflow.columns:
                cashflow[col] = cashflow[col].apply(to_num)
    # ----- BALANCE SHEET
    balancesheet = pd.DataFrame(j.get('data', {}).get('balancesheet', []))
    if not balancesheet.empty:
        balancesheet['company_id'] = cid
        balancesheet['year_orig'] = balancesheet['year']
        parsed = balancesheet['year_orig'].apply(parse_year_to_dt)
        balancesheet['year_dt'] = [p[0] for p in parsed]
        balancesheet['is_ttm'] = [p[1] for p in parsed]
        # numeric columns - skip 'year', 'company_id', 'equity_capital' as needed
        for col in balancesheet.columns:
            if col in ['id', 'company_id', 'year', 'year_orig', 'year_dt', 'is_ttm']:
                continue
            balancesheet[col] = balancesheet[col].apply(to_num)
    # ----- PROFIT & LOSS
    profitloss = pd.DataFrame(j.get('data', {}).get('profitandloss', []))
    if not profitloss.empty:
        profitloss['company_id'] = cid
        profitloss['year_orig'] = profitloss['year']
        parsed = profitloss['year_orig'].apply(parse_year_to_dt)
        profitloss['year_dt'] = [p[0] for p in parsed]
        profitloss['is_ttm'] = [p[1] for p in parsed]
        # numericize
        for col in profitloss.columns:
            if col in ['id', 'company_id', 'year', 'year_orig', 'year_dt', 'is_ttm']:
                continue
            profitloss[col] = profitloss[col].apply(to_num)

    # ----- ANALYSIS (pre-compiled)
    analysis_list = j.get('data', {}).get('analysis', [])
    # normalize: convert list-of-dict to dataframe, and attach company id & top-level meta
    analysis = pd.DataFrame(analysis_list)
    if not analysis.empty:
        analysis['company_id'] = cid
        # optionally add company-level info like roe/roce in company meta, if present
        for k in ('roce_percentage','roe_percentage'):
            if k in company_meta:
                analysis[k] = to_num(company_meta[k])
    
    # ----- Return everything
    return {
        'company_meta': company_meta,
        'cashflow': cashflow if not cashflow.empty else pd.DataFrame(),
        'balancesheet': balancesheet if not balancesheet.empty else pd.DataFrame(),
        'profitloss': profitloss if not profitloss.empty else pd.DataFrame(),
        'analysis': analysis if not analysis.empty else pd.DataFrame()
    }

# --- MAIN PIPELINE ---
def run_pipeline(limit=None, force_reprocess=False):
    # Silence specific warnings for cleaner output
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    files = sorted(glob.glob(file_glob))
    if limit:
        files = files[:limit]

    processed_cids = set()
    all_cf = []
    all_bs = []
    all_pl = []
    all_an = []
    all_meta = []

    for fp in tqdm(files, desc="Processing JSON files"):
        try:
            with open(fp, 'r', encoding='utf-8') as fh:
                head = json.load(fh).get('company', {})
                cid = head.get('id', Path(fp).stem)
        except Exception as e:
            print(f"Failed to read {fp}: {e}")
            continue
        if (cid in processed_cids) and not force_reprocess:
            continue

        out = process_json_file(fp)
        if not out['cashflow'].empty:
            all_cf.append(out['cashflow'])
        if not out['balancesheet'].empty:
            all_bs.append(out['balancesheet'])
        if not out['profitloss'].empty:
            all_pl.append(out['profitloss'])
        if not out['analysis'].empty:
            all_an.append(out['analysis'])
        if out['company_meta']:
            out_meta = out['company_meta'].copy()
            out_meta['company_id'] = cid
            all_meta.append(out_meta)

    # Save master DataFrames as CSV and log potential issues
    def concat_and_save_csv(new_list, csv_path, table_name):
        if new_list:
            new_df = pd.concat(new_list, ignore_index=True)
        else:
            new_df = pd.DataFrame()
        if new_df.empty:
            print(f"No data for {table_name}")
            return new_df
        try:
            new_df.to_csv(csv_path, index=False)
            print(f"Wrote {len(new_df)} rows to {csv_path}")
        except Exception as e:
            print(f"CSV write failed for {table_name}: {e}")
        return new_df

    master_cf = concat_and_save_csv(all_cf, csv_cashflow, 'cashflow')
    master_bs = concat_and_save_csv(all_bs, csv_balancesheet, 'balancesheet')
    master_pl = concat_and_save_csv(all_pl, csv_profitloss, 'profitloss')
    master_an = concat_and_save_csv(all_an, csv_analysis, 'analysis')

    # Save metadata about companies as CSV
    if all_meta:
        meta_df = pd.DataFrame(all_meta)
        # Drop columns with dict/list types
        for col in meta_df.columns:
            if meta_df[col].apply(lambda x: isinstance(x, (dict, list))).any():
                print(f"Dropping column '{col}' due to unsupported type for CSV.")
                meta_df = meta_df.drop(columns=[col])
        try:
            meta_df.to_csv(csv_meta, index=False)
            print(f"Wrote companies meta to {csv_meta}")
        except Exception as e:
            print(f"CSV write failed for meta_df: {e}")
    else:
        meta_df = pd.DataFrame()
        print("No meta_df to process or meta_df is empty.")

    # --- FEATURE ENGINEERING on master PL and BS ---
    if not master_pl.empty:
        if 'year_dt' not in master_pl.columns:
            master_pl['year_dt'] = pd.NaT
        master_pl['opm_calc'] = master_pl.apply(lambda r: (r['operating_profit'] / r['sales']) if (pd.notna(r.get('operating_profit')) and pd.notna(r.get('sales')) and r['sales'] != 0) else np.nan, axis=1)
        master_pl['npm_calc'] = master_pl.apply(lambda r: (r['net_profit'] / r['sales']) if (pd.notna(r.get('net_profit')) and pd.notna(r.get('sales')) and r['sales'] != 0) else np.nan, axis=1)
        master_pl['interest_cov'] = master_pl.apply(lambda r: (r['operating_profit'] / r['interest']) if (pd.notna(r.get('operating_profit')) and pd.notna(r.get('interest')) and r['interest'] != 0) else np.nan, axis=1)
        master_pl = master_pl.sort_values(['company_id','year_dt'])
        master_pl['sales_yoy'] = master_pl.groupby('company_id')['sales'].pct_change()
        master_pl['netprofit_yoy'] = master_pl.groupby('company_id')['net_profit'].pct_change()
        def compute_cagr(series):
            s = series.dropna()
            if len(s) < 2 or s.iloc[0] <= 0:
                return np.nan
            n = len(s) - 1
            return (s.iloc[-1] / s.iloc[0]) ** (1.0 / n) - 1.0
        try:
            cagr_sales = master_pl.groupby('company_id').apply(lambda g: compute_cagr(g.sort_values('year_dt')['sales'])).reset_index()
            cagr_sales.columns = ['company_id','sales_cagr']
        except Exception as e:
            print(f"CAGR sales calculation warning: {e}")
            cagr_sales = pd.DataFrame()
        try:
            cagr_net = master_pl.groupby('company_id').apply(lambda g: compute_cagr(g.sort_values('year_dt')['net_profit'])).reset_index()
            cagr_net.columns = ['company_id','netprofit_cagr']
        except Exception as e:
            print(f"CAGR net profit calculation warning: {e}")
            cagr_net = pd.DataFrame()
    else:
        cagr_sales = pd.DataFrame()
        cagr_net = pd.DataFrame()

    if not master_bs.empty:
        master_bs['leverage'] = master_bs.apply(lambda r: (r.get('borrowings') / r.get('total_assets')) if (pd.notna(r.get('borrowings')) and pd.notna(r.get('total_assets')) and r.get('total_assets') != 0) else np.nan, axis=1)
    # write results to sqlite for quick queries
    try:
        conn = sqlite3.connect(sqlite_db)
        if not master_cf.empty:
            master_cf.to_sql('cashflow', conn, if_exists='replace', index=False)
        if not master_bs.empty:
            master_bs.to_sql('balancesheet', conn, if_exists='replace', index=False)
        if not master_pl.empty:
            master_pl.to_sql('profitloss', conn, if_exists='replace', index=False)
        if not master_an.empty:
            master_an.to_sql('analysis', conn, if_exists='replace', index=False)
        if not meta_df.empty:
            meta_df.to_sql('companies_meta', conn, if_exists='replace', index=False)
        if not cagr_sales.empty:
            cagr_sales.to_sql('sales_cagr', conn, if_exists='replace', index=False)
        if not cagr_net.empty:
            cagr_net.to_sql('netprofit_cagr', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Wrote SQLite DB to {sqlite_db}")
    except Exception as e:
        print("SQLite write failed:", e)

    return {
        'cashflow': master_cf,
        'balancesheet': master_bs,
        'profitloss': master_pl,
        'analysis': master_an,
        'meta': meta_df,
        'sales_cagr': cagr_sales,
        'net_cagr': cagr_net
    }

# Run (use limit=5 while testing)
if __name__ == '__main__':
    results = run_pipeline(limit=process_limit, force_reprocess=False)
    print("Done. Master files placed in:", output_dir)
