# Task 1: API Integration & Data Fetching

## Status
**Done**

## Description
Build a Python module to read company IDs from the Excel sheet (`Nifty100Companies`) and fetch financial data (Balance Sheet, P&L, and Cash Flow) using the provided API. Ensure proper error handling (timeouts, invalid IDs, retries) and logging for each API request.

---

## Subtasks

1. **Load Excel and Extract Company IDs**
    - Read the Excel file and extract the list of company IDs.

2. **Loop Through Each ID and Call the API**
    - Iterate over each company ID and make API requests for financial data.

3. **Parse JSON Responses and Validate Required Fields**
    - Parse the API's JSON responses and check for the presence of required fields.

4. **Handle API Failures, Log Errors, and Retry if Needed**
    - Implement error handling for timeouts, invalid IDs, and failed requests.
    - Log each API request and error for traceability.
    - Retry failed requests as necessary.

5. **Store Raw Data Locally as JSON (Optional for Debugging)**
    - Optionally, save the raw API responses as JSON files for debugging purposes.

---

## Notes
- Ensure robust error handling and logging throughout the process.
- Validate all required fields in the API response before processing.
- Use environment variables or configuration files for sensitive information (e.g., API keys).
- Consider using libraries such as `pandas` for Excel handling and `requests` for API calls.
