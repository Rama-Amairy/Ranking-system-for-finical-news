from loguru import logger
import os


class Logger:
    """
    A configurable logging class using Loguru.

    Attributes:
        log_name (str): Name of the log file.
        log_dir (str): Directory where logs are stored.
        log_size (str): Maximum size of log files before rotation.
        level (str): Logging level (e.g., INFO, DEBUG, ERROR).
    """

    def __init__(
        self, log_name="pipeline", log_dir="logs", log_size="1 MB", level="INFO"
    ):
        """
        Initializes the Logger class with specified configurations.

        Args:
            log_name (str): The name of the log file (default: "pipeline").
            log_dir (str): Directory where logs will be stored (default: "logs").
            log_size (str): Maximum size of a log file before rotation (default: "1 MB").
            level (str): Logging level (default: "INFO").
        """
        self.log_dir = log_dir
        self.log_name = log_name
        self.log_size = log_size
        self.level = level
        self._setup()

    def _setup(self):
        """
        Sets up the logging configuration by creating the log directory
        (if it doesn't exist) and adding a log file with rotation.
        """
        os.makedirs(self.log_dir, exist_ok=True)
        log_path = os.path.join(self.log_dir, f"{self.log_name}.log")
        logger.add(log_path, rotation=self.log_size, level=self.level)
        logger.info("Logging initialized.")

    @staticmethod
    def get_logger():
        """
        Returns the logger instance.

        Returns:
            logger: The Loguru logger instance.
        """
        return logger


# Example usage
# log_instance = Logger()
# logger = log_instance.get_logger()
