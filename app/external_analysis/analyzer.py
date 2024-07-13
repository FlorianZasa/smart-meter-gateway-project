import logging

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Logging: Log Level selectable depending on importance. INFO is good for audit logs.
handler = logging.FileHandler('external_analysis.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_external_access(action, username):
    """Log external access

    Args:
        action (str): The action performed (e.g., 'login', 'register')
        username (str): The username of the user who performed the action
    """
    logger.info(f"External access: {action} - User: {username}")

def log_data_access(action, user_id):
    """Log data access

    Args:
        action (str): The action performed (e.g., 'get_consumption', 'add_consumption')
        user_id (str): The user ID of the user who performed the action
    """
    logger.info(f"Data access: {action} - User ID: {user_id}")

def analyze_logs():
    """Analyze logs for suspicious activities

    This function could be implemented to analyze the logs for any suspicious activities.
    """
    pass