import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:

    DATABASE_FILENAME : str = os.getenv("DATABASE_FILENAME")
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = f"sqlite:///{PROJECT_DIR}{DATABASE_FILENAME}"

settings = Settings()