import os
import json
import logging
from pathlib import Path

def setup_google_cloud_credentials():
    """
    Setup Google Cloud credentials for TTS
    
    This function checks for credentials in the following order:
    1. GOOGLE_APPLICATION_CREDENTIALS environment variable
    2. .env file GOOGLE_CLOUD_CREDENTIALS_PATH
    3. Default service account key location
    
    Returns:
        str: Path to credentials file or None if not found
    """
    
    # Check environment variable
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_path and os.path.exists(creds_path):
        logging.info(f"Using Google Cloud credentials from GOOGLE_APPLICATION_CREDENTIALS: {creds_path}")
        return creds_path
    
    # Check .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    creds_path = os.getenv('GOOGLE_CLOUD_CREDENTIALS_PATH')
    if creds_path and os.path.exists(creds_path):
        logging.info(f"Using Google Cloud credentials from .env file: {creds_path}")
        return creds_path
    
    # Check default locations
    default_paths = [
        'config/google-cloud-credentials.json',
        'google-cloud-credentials.json',
        os.path.expanduser('~/.config/gcloud/application_default_credentials.json')
    ]
    
    for path in default_paths:
        if os.path.exists(path):
            logging.info(f"Using Google Cloud credentials from default location: {path}")
            return path
    
    logging.warning("No Google Cloud credentials found. Google TTS will not be available.")
    return None

def validate_google_cloud_credentials(credentials_path):
    """
    Validate Google Cloud credentials file
    
    Args:
        credentials_path: Path to the credentials JSON file
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not credentials_path or not os.path.exists(credentials_path):
        return False
    
    try:
        with open(credentials_path, 'r') as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        
        for field in required_fields:
            if field not in creds:
                logging.error(f"Missing required field in credentials: {field}")
                return False
        
        if creds.get('type') != 'service_account':
            logging.error("Credentials file is not for a service account")
            return False
        
        logging.info("Google Cloud credentials validated successfully")
        return True
        
    except json.JSONDecodeError:
        logging.error("Invalid JSON in credentials file")
        return False
    except Exception as e:
        logging.error(f"Error validating credentials: {e}")
        return False

def create_sample_env_file():
    """Create a sample .env file with Google Cloud TTS configuration"""
    sample_content = """
# Google Cloud TTS Configuration
# Uncomment and set the path to your Google Cloud service account JSON file
# GOOGLE_CLOUD_CREDENTIALS_PATH=path/to/your/google-cloud-credentials.json

# Alternative: Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
# GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-cloud-credentials.json

# Enable Google TTS (set to true to use Google TTS instead of Coqui TTS)
USE_GOOGLE_TTS=false

# Existing configuration
HF_TOKEN="your_huggingface_token"
Groq_TOKEN="your_groq_token"
"""
    
    env_file_path = '.env.sample'
    if not os.path.exists(env_file_path):
        with open(env_file_path, 'w') as f:
            f.write(sample_content.strip())
        print(f"Sample environment file created: {env_file_path}")
        print("Copy this to .env and configure your Google Cloud credentials")