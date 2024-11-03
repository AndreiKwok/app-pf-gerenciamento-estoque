"""
    Import all libraries bibliotecas what i am using at the script
"""
import logging
import  sys
import os

class LoggerSetup:
    '''
        Defining the metod launcher qhat go to to receive
        pathLog -> path where go to stay the file of LOG
        nameLog -> name of log
        nameLogger -> The name of logger what it will be armazenado at the system
    '''

    def __init__(self, pathLog,
                 nameLog,
                 nameLogger):

        self._pathLog: str = pathLog
        self._nameLog: str = nameLog
        self._nameLogger: str = nameLogger


    '''
        Defining the configuration basic standard what is used us logs
        Configuration basic
        Create and configure the formatter
        Get the pth where the log it will be 
        Create one logger with the name que be being received at variable
        Create one manipulator im files
    '''

    def _setup_logger(self, levellOG: str = None):
        # Configure basic logging settings
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        # Create and configure the formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Get the path where the log will be stored
        log_path = os.path.join(self._pathLog, self._nameLog)

        # Create a logger with the name provided
        logger = logging.getLogger(self._nameLogger)
        logger.setLevel(logging.DEBUG)

        # Create a file handler for logging to a file
        file_handler = logging.FileHandler(log_path)

        # Convert the string level to the corresponding logging level
        level = getattr(logging, levellOG.upper(), logging.DEBUG)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(file_handler)

        return logger

    # Create functions to log messages with different levels
    def debugMessage(self, message: str = None, level: str = None):
        self._logger = self._setup_logger(level)
        self._logger.debug(message)

    def infoMessage(self, message: str = None, level: str = None):
        self._logger = self._setup_logger(level)
        self._logger.info(message)

    def errorMessage(self, message: str = None, level: str = None):
        self._logger = self._setup_logger(level)
        self._logger.error(message)

    def warningMessage(self, message: str = None, level: str = None):
        self._logger = self._setup_logger(level)
        self._logger.warning(message)
    
    def ignor(self, log_specify: str = None, level: str = None):
        self.__level = getattr(logging, level.upper(), logging.WARNING)
        
        logging.getLogger(log_specify).setLevel(self.__level)