# ML Results Migration & Upsert Plan

## 1. Confirm Prerequisites
- **Back Up Your DB:** If this is not a development copy, create a backup before proceeding.
- **User Privileges:** Ensure your MySQL/MariaDB user has `CREATE`, `ALTER`, `INSERT`, `UPDATE`, `SELECT` privileges on the target schema.
- **Check Version:** Run the following in your SQL client to determine your database version:
    ```sql
    SELECT VERSION();
    ```
    - If **MariaDB 10.5+** or **MySQL 8.0+**, you can use the `JSON_ARRAYAGG` function.
    - Otherwise, use the `GROUP_CONCAT` approach.

## 2. Sanity Check Existing Schema
- Confirm `companies.id` is `VARCHAR(255)` (or adjust the `ml` table definition to match).

## 3. Create the `ml` Table
- Run the following SQL (adjust `VARCHAR(255)` if your `companies.id` uses a different type/length):
    ```sql
    CREATE TABLE ml (
        company_id VARCHAR(255) PRIMARY KEY,
        results JSON NOT NULL
    );
    ```

## 4. Migrate Existing Data
- **For MySQL 8.0+ or MariaDB 10.5+ (with `JSON_ARRAYAGG`):**
    ```sql
    INSERT INTO ml (company_id, results)
    SELECT company_id, JSON_ARRAYAGG(result_column) FROM old_ml_results GROUP BY company_id;
    ```
- **For MySQL 5.7 or MariaDB <10.5 (no `JSON_ARRAYAGG`):**
    ```sql
    INSERT INTO ml (company_id, results)
    SELECT company_id, CONCAT('[', GROUP_CONCAT(result_column), ']') FROM old_ml_results GROUP BY company_id;
    ```

## 5. Verify Migration
- Run:
    ```sql
    SELECT * FROM ml;
    ```
- Ensure all `results` values are valid JSON.

## 6. Python Upsert Script
- Copy the provided `save_ml_results_tailored.py` into `Task_4/save_ml_results_tailored.py`.
- **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
- **Run the script** (adjust paths and credentials as needed):
    ```bash
    python Task_4/save_ml_results_tailored.py
    ```

## 7. Smoke Test Reads
- Run a simple SELECT to verify data integrity:
    ```sql
    SELECT * FROM ml LIMIT 5;
    ```

## 8. (Optional) Scheduling
- Automate the upsert script to run after each ML process.
- Add additional indexes if required for performance.

## 9. Rollback
- To revert, restore your database from the backup created in Step 1.

---

You are now ready to proceed. If you would like assistance creating the Python upsert script or guidance on any specific step, please let me know!