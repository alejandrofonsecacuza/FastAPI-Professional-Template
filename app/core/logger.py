import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from app.core.config import settings

class CustomLogger:
    """
    Professional logging configuration.
    Initializes automatically on import.
    """
    def __init__(self):
        self.log_dir = settings.LOG_DIR
        self.log_file = os.path.join(self.log_dir, settings.LOG_FILENAME)
        self._create_log_dir()
        self.logger = self._setup_logger()

    def _create_log_dir(self):
        """Ensures the log directory exists."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _setup_logger(self):
        formatter = logging.Formatter(
            fmt=settings.LOG_FORMAT,
            datefmt=settings.LOG_DATETIME_FORMAT
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # Rotates when file reaches 10MB, keeps 5 backup files
        file_handler = RotatingFileHandler(
            filename=self.log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.setLevel(settings.LOG_LEVEL)
        
        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

        return root_logger

logger = CustomLogger().logger