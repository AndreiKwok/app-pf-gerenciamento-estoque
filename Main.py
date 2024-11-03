from fastapi import FastAPI, APIRouter  # Import FastAPI for creating the web service and APIRouter for handling routing
from src.Fast.Fast import router  # Import the router from your Fast module for including in the main app
from Log.Log import LoggerSetup  # Import LoggerSetup for logging messages
import os
# Initialize the logger with the path for storing logs, the log file name, and a log label
log = LoggerSetup(
    fr'{os.getcwd()}\Logs',
    'Log_main.log',
    'Main Logger'
)
print(fr'{os.getcwd()}\Logs')

try:
    log.infoMessage('Main is Run', 'INFO')  # Log an info message indicating that the main application is starting
    app = FastAPI()  # Create an instance of the FastAPI application
    app.include_router(router)  # Include the router with all the defined routes from the Fast module
    
except Exception as e:  # Catch any exceptions that occur during initialization
    log.errorMessage(e, 'ERROR')  # Log the error message if an exception is caught
