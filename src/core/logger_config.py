import os
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

def setup_logger(name='AetherLogger'):
    """
    Configura y retorna un logger con salida a consola y archivo.
    El nivel se define desde .env con LOG_LEVEL.
    """
    logger = logging.getLogger(name)
    logger.setLevel(os.getenv('LOG_LEVEL', 'INFO').upper())
    logger.propagate = False
    
    if not logger.handlers:
        log_format = logging.Formatter(
            fmt='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)
        
        if getattr(sys, 'frozen', False):
            BASE_DIR = Path(sys.executable).parent
        else:
            BASE_DIR = Path(__file__).resolve().parents[2]
        
        log_dir = os.path.join(BASE_DIR, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            filename=os.path.join(log_dir, 'app.log'),
            maxBytes=5_000_000, # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
        
    return logger