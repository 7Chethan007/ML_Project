import logging
from colorama import init, Fore, Style
from datetime import datetime
import os

# Initialize colorama for Windows
init(autoreset=True)

# Set up logging to file (no color codes)
logging.basicConfig(
    filename='log.txt',
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)

def log_success(msg):
    print(Fore.GREEN + msg)
    logging.info(msg)

def log_error(msg):
    print(Fore.RED + msg)
    logging.error(msg)

def log_info(msg):
    print(msg)
    logging.info(msg)

def print_company_result(company_id, company_name, pros, cons, idx, total):
    print(f"{Style.BRIGHT}Processing: {company_name} (ID: {company_id})")
    logging.info(f"Processing: {company_name} (ID: {company_id})")
    print(Fore.GREEN + "    Pros:")
    logging.info("    Pros:")
    for p in pros[:4]:
        print(Fore.GREEN + f"        - {p['text']}")
        logging.info(f"        - {p['text']}")
    print(Fore.RED + "    Cons:")
    logging.info("    Cons:")
    for c in cons[:4]:
        print(Fore.RED + f"        - {c['text']}")
        logging.info(f"        - {c['text']}")
    print(f"Progress: {idx}/{total} companies processed\n")
    logging.info(f"Progress: {idx}/{total} companies processed")

# Example usage (remove or adapt in your main script):
if __name__ == "__main__":
    # Example data
    companies = [
        {
            'company_id': '12345',
            'company_name': 'Acme Corp',
            'pros': [{'text': 'Great work-life balance'}, {'text': 'Competitive salary'}],
            'cons': [{'text': 'Long commute'}, {'text': 'Outdated technology'}]
        },
        {
            'company_id': '67890',
            'company_name': 'Beta Inc',
            'pros': [{'text': 'Flexible hours'}],
            'cons': [{'text': 'Low pay'}]
        }
    ]
    total = len(companies)
    for idx, rec in enumerate(companies, 1):
        try:
            print_company_result(rec['company_id'], rec['company_name'], rec['pros'], rec['cons'], idx, total)
            # Simulate success
            log_success(f"[Success] Analysis completed for {rec['company_name']} (ID: {rec['company_id']})")
        except Exception as e:
            log_error(f"[Error] Failed to process {rec.get('company_name', '')} (ID: {rec.get('company_id', '')}): {e}")
