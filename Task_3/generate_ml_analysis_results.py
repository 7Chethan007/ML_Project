import os
import json

DATA_DIR = "C:/Users/Chethan/OneDrive/Desktop/Summer/1SDE/ML_Project/data"
OUTPUT_PATH = "C:/Users/Chethan/OneDrive/Desktop/Summer/1SDE/ML_Project/Task_3/ml_analysis_results.json"

def extract_analysis(company_id, data):
    # Extract company name
    company_name = data.get("company", {}).get("company_name", company_id)

    # Extract pros and cons as raw string (for MySQL compatibility)
    prosandcons = data.get("data", {}).get("prosandcons", [])
    if prosandcons:
        pros = prosandcons[0].get("pros", "")
        cons = prosandcons[0].get("cons", "")
    else:
        pros, cons = "", ""

    # Extract analysis (find 3, 5, 10 year growth and ROE)
    analysis_list = data.get("data", {}).get("analysis", [])
    analysis_json = {}
    for period, key in [("3 Years", "3"), ("5 Years", "5"), ("10 Years", "10")]:
        for a in analysis_list:
            if period in a.get("compounded_sales_growth", ""):
                analysis_json.setdefault("compounded_sales_growth", {})[key] = a["compounded_sales_growth"]
            if period in a.get("compounded_profit_growth", ""):
                analysis_json.setdefault("compounded_profit_growth", {})[key] = a["compounded_profit_growth"]
            if period in a.get("roe", ""):
                analysis_json.setdefault("roe", {})[key] = a["roe"]

    return {
        "company_id": company_id,
        "company_name": company_name,
        "pros": pros,
        "cons": cons,
        "analysis_json": analysis_json
    }

def main():
    results = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".json"):
            company_id = fname.replace(".json", "")
            with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
            analysis = extract_analysis(company_id, data)
            results.append(analysis)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(results)} company analyses to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()