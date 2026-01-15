import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from src.core.logger_config import setup_logger
from src.core.config import get_dynamic_paths
from src.processors.xlsx_to_txt_converter import process_xlsx_file

logger = setup_logger()

class EventoDeEntrada(FileSystemEventHandler):
    """
    Handler personalizado para eventos en la carpeta de Entrada.
    Detecta archivos .xlsx nuevos y lanza el procesamiento correspondiente.
    """
    def __init__(self, entrada_path):
        self.entrada_path = entrada_path

    def _procesar(self, event, tipo_evento):
        """Método interno para validar y procesar el archivo."""
        if not event.is_directory and event.src_path.lower().endswith(".xlsx") and "~$" not in event.src_path:
            time.sleep(1)
            try:
                logger.info(f"Detectado nuevo archivo: {event.src_path}")
                process_xlsx_file(
                    event.src_path
                )
            except Exception as e:
                logger.error(f"Error al procesar archivo {event.src_path}: {e}")
        
    def on_created(self, event):
        """Se activa al pegar o mover un archivo nuevo a la carpeta."""
        self._procesar(event, "CREACION")

    def on_modified(self, event):
        """Se activa al guardar cambios en un archivo existente."""
        self._procesar(event, "MODIFICACION")
                
def iniciar():
    """
    Inicia el observador de watchdog sobre la carpeta Entrada.
    """
    rutas = get_dynamic_paths()
    entrada_path = rutas['entrada']
    
    event_handler = EventoDeEntrada(entrada_path)
    observer = Observer()
    observer.schedule(event_handler, entrada_path, recursive=False)
    observer.start()
    
    logger.info(f"Monitoreando carpeta: {entrada_path}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Deteniendo el monitor...")
        observer.stop()
    except Exception as e:
        logger.error(f"Error inesperado en el monitor: {e}")
    
    observer.join()