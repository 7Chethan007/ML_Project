import json
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

CREATE_ML_SQL = """
CREATE TABLE IF NOT EXISTS ml (
  company_id VARCHAR(255) NOT NULL PRIMARY KEY,
  company_name VARCHAR(255),
  pros JSON,
  cons JSON,
  analysis_json JSON,
  last_updated DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

UPSERT_ML_SQL = """
INSERT INTO ml (company_id, company_name, pros, cons, analysis_json, last_updated)
VALUES (:company_id, :company_name, :pros, :cons, :analysis_json, :last_updated)
ON DUPLICATE KEY UPDATE
  company_name = VALUES(company_name),
  pros = VALUES(pros),
  cons = VALUES(cons),
  analysis_json = VALUES(analysis_json),
  last_updated = VALUES(last_updated);
"""


def get_engine(user, password, host, port, db):
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"
    return create_engine(url, pool_size=5, max_overflow=10, pool_recycle=3600)

def prepare_record(rec):
    return {
        'company_id': rec['company_id'],
        'company_name': rec.get('company_name'),
        'pros': json.dumps(rec.get('pros', []), ensure_ascii=False),
        'cons': json.dumps(rec.get('cons', []), ensure_ascii=False),
        'analysis_json': json.dumps(rec, ensure_ascii=False),
        'last_updated': datetime.utcnow()
    }

def upsert_batch(engine: Engine, records):
    with engine.begin() as conn:
        conn.execute(text(CREATE_ML_SQL))
        prepared = [prepare_record(r) for r in records]
        conn.execute(text(UPSERT_ML_SQL), prepared)
    print(f"Upserted {len(records)} records into ml.")

def load_results(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and 'results' in data:
        return data['results']
    return data

if __name__ == "__main__":
    # Fill in your DB credentials and result file path
    url = "mysql+pymysql://root:Chethan%40007@127.0.0.1:3306/ml?charset=utf8mb4"
    engine = create_engine(url)

    recs = load_results("C:/Users/Chethan/OneDrive/Desktop/Summer/1SDE/ML_Project/Task_3/ml_analysis_results.json")
    upsert_batch(engine, recs)