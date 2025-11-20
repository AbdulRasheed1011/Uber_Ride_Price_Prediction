import logging
from datetime import datetime
from pathlib import Path

# Create a folder for logs if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Path for login log file
LOG_FILE = "logs/login_activity.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_login(username: str):
    logging.info(f"User logged in: {username}")

def log_logout(username: str):
    logging.info(f"User logged out: {username}")



if __name__ == "__main__":
    log_login("Rasheed")
    log_logout("Rasheed")
    print("Login events logged!")