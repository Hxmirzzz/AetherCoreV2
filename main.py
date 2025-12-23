import time
from watchdog.observers import Observer
from src.core.monitor import EventoDeEntrada
from src.core.config import get_dynamic_paths
from src.core.logger_config import setup_logger

logger = setup_logger()

def main():
    """
    Punto de entrada del sistema AetherCore2.
    Monitorea la carpeta de entrada para detectar archivos .xlsx nuevos.
    """
    paths = get_dynamic_paths()
    input_path = paths["entrada"]
    
    logger.info("Iniciando AetherCore2...")
    logger.info(f"Esperando archivos en: {input_path}")
    
    event_handler = EventoDeEntrada(input_path)
    observer = Observer()
    observer.schedule(event_handler, path=input_path, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1) #Evitar sobrecarga de CPU
    except KeyboardInterrupt:
        logger.info("Finalizando monitoreo...")
        observer.stop()
        
    observer.join()
    
if __name__ == "__main__":
    main()