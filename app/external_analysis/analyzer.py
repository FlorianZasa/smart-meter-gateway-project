import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('external_analysis.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_external_access(action, username):
    logger.info(f"External access: {action} - User: {username}")

def log_data_access(action, user_id):
    logger.info(f"Data access: {action} - User ID: {user_id}")

def analyze_logs():
    # Hier könnte eine Analyse der Logs implementiert werden
    pass