import logging
from colorama import init, Fore, Style

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
