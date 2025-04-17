import logging
import os
from datetime import datetime

FILE_NAME = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = os.path.join(os.path.dirname(__file__), f"logs/{FILE_NAME}.log")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), f"logs/{FILE_NAME}.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
