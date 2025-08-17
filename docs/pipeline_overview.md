# Pipeline Overview

This document provides a high-level overview of the ML Project pipeline.

## Steps
1. **Data Fetching:** Download and collect company data from APIs or files.
2. **Data Preprocessing:** Clean and prepare data for analysis.
3. **ML Analysis:** Run machine learning scripts to generate insights (pros, cons, growth, etc).
4. **Database Storage:** Store results in the MySQL `ml` table using upsert scripts.
5. **Real-time Logging:** Monitor progress and errors in the terminal and log file.
6. **Web Frontend:** Dynamically display results for each company and in list view.

See the [setup guide](setup_guide.md) for installation and [usage guide](usage_guide.md) for running the pipeline.
