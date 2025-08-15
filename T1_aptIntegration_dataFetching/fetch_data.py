
import pandas as pd
import requests
import os
import logging
from time import sleep
from dotenv import load_dotenv

# Load environment variables from .env file in the parent directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# --- Configuration ---
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
COMPANY_LIST_PATH = os.path.join("..", "company_id.xlsx")
OUTPUT_DIR = os.path.join("..", "data")
LOG_FILE = "data_fetching.log"
REQUEST_TIMEOUT = 10  # seconds
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def load_company_ids(file_path):
    """Loads company IDs from the specified Excel file."""
    try:
        df = pd.read_excel(file_path)
        if "company_id" not in df.columns:
            logging.error("'company_id' column not found in the Excel file.")
            return []
        return df["company_id"].dropna().unique().tolist()
    except FileNotFoundError:
        logging.error(f"Error: The file at {file_path} was not found.")
        return []
    except Exception as e:
        logging.error(f"An error occurred while reading the Excel file: {e}")
        return []

def fetch_financial_data(company_id):
    """Fetches financial data for a given company ID with retry logic."""
    params = {"id": company_id, "api_key": API_KEY}
    for attempt in range(RETRY_ATTEMPTS):
        try:
            response = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # The API returns a 200 OK with "No Data Found" for invalid IDs
            if "No Data Found" in response.text:
                logging.warning(f"No data found for company ID: {company_id}. Skipping.")
                return None

            return response.json()

        except requests.exceptions.Timeout:
            logging.warning(f"Request for {company_id} timed out. Attempt {attempt + 1} of {RETRY_ATTEMPTS}.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request for {company_id} failed: {e}. Attempt {attempt + 1} of {RETRY_ATTEMPTS}.")
        
        if attempt < RETRY_ATTEMPTS - 1:
            sleep(RETRY_DELAY)
    
    logging.error(f"Failed to fetch data for {company_id} after {RETRY_ATTEMPTS} attempts.")
    return None

def save_data_to_json(data, company_id, directory):
    """Saves the fetched data to a JSON file."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"{company_id}.json")
    try:
        with open(file_path, "w") as f:
            import json
            json.dump(data, f, indent=4)
        logging.info(f"Successfully saved data for {company_id} to {file_path}")
    except IOError as e:
        logging.error(f"Failed to write data to {file_path}: {e}")

def main():
    """Main function to orchestrate the data fetching process."""
    logging.info("--- Starting Financial Data Fetching Process ---")
    
    company_ids = load_company_ids(COMPANY_LIST_PATH)
    if not company_ids:
        logging.error("No company IDs loaded. Exiting.")
        return

    logging.info(f"Loaded {len(company_ids)} unique company IDs.")

    for company_id in company_ids:
        logging.info(f"Fetching data for company: {company_id}")
        financial_data = fetch_financial_data(company_id)
        if financial_data and 'data' in financial_data:
            # The actual financial data is nested under the 'data' key
            data_to_save = financial_data['data']
            
            # Basic validation on the nested data object
            if "balance_sheet" in data_to_save and "profit_and_loss" in data_to_save and "cash_flow" in data_to_save:
                 save_data_to_json(data_to_save, company_id, OUTPUT_DIR)
            else:
                logging.warning(f"Validation failed for {company_id}. Missing one or more required fields in the 'data' object.")
                # Still save the nested 'data' object for inspection
                save_data_to_json(data_to_save, company_id, OUTPUT_DIR)
        elif financial_data:
            logging.warning(f"Response for {company_id} does not contain a 'data' key. Saving entire response for inspection.")
            save_data_to_json(financial_data, company_id, OUTPUT_DIR)

    logging.info("--- Financial Data Fetching Process Finished ---")

if __name__ == "__main__":
    main()