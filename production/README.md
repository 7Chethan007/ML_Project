# Production ML Financial Analysis Pipeline

This directory contains the production-ready code for the end-to-end ML financial analysis pipeline, including data fetching, preprocessing, ML analysis, MySQL upsert, real-time logging, and a PHP web frontend.

---

## Directory Structure

```
production/
│
├── pipeline.ipynb           # Unified notebook: data fetching, preprocessing, ML analysis, MySQL upsert
├── realtime_logger.py       # Importable logger module
├── requirements.txt         # Python dependencies
├── .env.example            # Template for environment variables
├── web/                     # PHP web frontend
│   ├── index.php
│   ├── company.php
│   ├── db.php
│   └── assets/              # (Add CSS/JS/images if needed)
```

---

## 1. Setup Python Environment

1. Create a virtual environment (recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API keys and DB credentials:
   ```powershell
   copy .env.example .env
   # Edit .env with your values
   ```

---

## 2. Run the Pipeline

Open and run all cells in `pipeline.ipynb` to:
- Fetch company data from the API
- Preprocess and aggregate data
- Run ML analysis
- Upsert results into MySQL

All logs will be written to `log.txt` and printed in real-time.

---

## 3. Deploy the Web Frontend

1. Ensure your MySQL server is running and the `ml` database is populated.
2. Copy the `web/` folder to your PHP server's root (e.g., `htdocs` for XAMPP or `www` for WAMP/LAMP).
3. Set environment variables for DB credentials (or edit `db.php` to hardcode if needed).
4. Start your PHP server:
   ```powershell
   # Example for built-in PHP server
   cd web
   php -S localhost:8000
   ```
5. Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 4. Notes
- For production, never commit your real `.env` file or credentials.
- Update `requirements.txt` if you add new Python dependencies.
- For any issues, check `log.txt` for details.

---

## Author
Project by Chethan M N
