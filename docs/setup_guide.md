# Setup Guide

## Prerequisites
- Python 3.8+
- MySQL 8.0+ (or MariaDB 10.5+)
- PHP 8+
- Composer (optional, for PHP dependencies)

## Installation Steps
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd ML_Project
   ```
2. **Set up Python environment:**
   ```bash
   python -m venv ml_proj
   ml_proj\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
3. **Set up MySQL database:**
   - Import `ml.sql` or use `docs/ml_table_schema.sql` for schema only.
   - Ensure your `.env` file has correct DB credentials.
4. **Enable PHP extensions:**
   - Edit `php.ini` and enable `mysqli` and `pdo_mysql`.
5. **Start the PHP server:**
   ```bash
   cd Task_6
   php -S localhost:8000
   ```
6. **Open the web frontend:**
   - Go to [http://localhost:8000](http://localhost:8000)

See [usage guide](usage_guide.md) for running the pipeline.
