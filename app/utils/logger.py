import logging
from datetime import datetime
import time
import os
from pathlib import Path

class CustomLogger:
    def __init__(self, module_name):
        self.module_name = module_name
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.INFO)
        
        # Crear directorio de logs si no existe
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Formato consistente con tu estructura original
        formatter = logging.Formatter(
            '%(asctime)s|%(custom_module)s|%(custom_api)s|%(custom_function)s|%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Handler para archivo (con rotación diaria)
        file_handler = logging.FileHandler(
            filename=logs_dir / 'monitoring.log',
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # Limpiar handlers existentes y añadir los nuevos
        self.logger.handlers.clear()
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # Evitar propagación al logger root
        self.logger.propagate = False
    
    def log(self, api_name, function_name, message, start_time=None):
        """
        Registra un mensaje con:
        - api_name: Nombre de la API (ej. "pokeapi")
        - function_name: Nombre de la función (ej. "get_pokemon")
        - message: Mensaje descriptivo
        - start_time: Timestamp para calcular latencia (opcional)
        """
        try:
            if start_time:
                latency = int((time.time() - start_time) * 1000)  # in ms
                message = f"{message} | Latency: {latency}ms"
            
            extra = {
                'custom_module': self.module_name,
                'custom_api': api_name,
                'custom_function': function_name
            }
            
            self.logger.info(
                message,
                extra=extra
            )
            return time.time()
            
        except Exception as e:
            # Fallback seguro si hay error con los campos personalizados
            self.logger.error(
                f"Logging error | Module: {self.module_name} | API: {api_name} | Error: {str(e)}",
                extra={
                    'custom_module': 'Logger',
                    'custom_api': 'log',
                    'custom_function': 'error_handling'
                }
            )
            return time.time()