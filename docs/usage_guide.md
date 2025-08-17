# Usage Guide

## Running the Pipeline

1. **Fetch Data:**
   - Run the data fetching script:
     ```bash
     python Task_1/fetch_data.py
     ```
2. **Preprocess Data:**
   - Run preprocessing:
     ```bash
     python Task_2/data_preprocessing.py
     ```
3. **Run ML Analysis:**
   - Use the analysis notebook or script:
     ```bash
     jupyter notebook Task_3/ml_analysis.ipynb
     # or
     python Task_3/ml_analysis.py
     ```
4. **Upsert Results to MySQL:**
   - Run the upsert script:
     ```bash
     python Task_4/save_ml_results_tailored.py
     ```
5. **View Results:**
   - In terminal: See real-time output and logs in `log.txt`.
   - In browser: Open [http://localhost:8000](http://localhost:8000) for the web frontend.

## Troubleshooting
- Check `log.txt` for errors.
- Ensure MySQL and PHP servers are running.
- See [setup guide](setup_guide.md) for environment help.
