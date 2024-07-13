import os
from dotenv import load_dotenv
from pathlib import Path

# Lade alle Umgebungsvariables von der .env Datei
base_dir = Path(__file__).resolve().parent
load_dotenv(base_dir / '.env')

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    WAN_HOST = os.getenv('WAN_HOST')
    WAN_PORT = int(os.getenv('WAN_PORT'))
    LAN_HOST = os.getenv('LAN_HOST')
    LAN_PORT = int(os.getenv('LAN_PORT'))
    LAN_IP_RANGES = os.getenv('LAN_IP_RANGES')