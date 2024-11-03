from src.Responses.Response import Response  # Import the Response class from your custom responses module
from fastapi import FastAPI, APIRouter  # Import FastAPI and APIRouter for creating the web service
from httpx import AsyncClient, Timeout, HTTPStatusError  # Import AsyncClient for making async HTTP requests
from Log.Log import LoggerSetup  # Import LoggerSetup for logging error messages
import asyncio  # Import asyncio for handling asynchronous operations
import os


# Create an APIRouter instance with a prefix '/fast' for organizing the routes
router = APIRouter(prefix='/fast')
resp = Response()  # Create an instance of the Response class to handle response-related operations

# Initialize the logger with the path for storing logs, the log file name, and a log label
log = LoggerSetup(
    fr'{os.getcwd()}\Logs',
    'Log_FastApi.log',
    'FastApi Logger'
)

@router.get("/items")  # Define a GET endpoint for retrieving item information
async def read_item(item: str = None):
    """
    Endpoint that checks the status of `/items/put_buy` and returns the query data.
    """
    try:
        # Call the method to get the item details for 'Galaxy ZFlip'
        response = await resp.get_query_consult_itens_product('Galaxy ZFlip')
        # Prepare a list of tuples with key-value pairs from the response
        values = [(key, value) for key, value in response.items()]

        return {'item': f'{values}'}  # Return the item details as a response

    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message

@router.get("/items/put_buy")  # Define a GET endpoint for purchasing an item
async def buy(): 
    try:
        # Call the method to buy an item ('Galaxy S100') with a specified quantity (1)
        response = await resp.get_buy_item("Galaxy S25 Ultra", 1)
        # Prepare a list of tuples with key-value pairs from the response
        values = [(key, value) for key, value in response.items()]

        return {'item purchased': f'product {values} bought.'}  # Return a success message with the bought item details

    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message

@router.get("/items/post_item")  # Define a GET endpoint for inserting a new item
async def insert(): 
    try:
        # Call the method to insert a new item into the database
        response = await resp.get_insert_document('Galaxy S24 Ultra', 10, 5.600, 'Celular')
        return {"message": f"{response}"}  # Return a success message
    
    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message

@router.get("/item/put_item")  # Define a GET endpoint for inserting a new item
async def insert_unique_value(): 
    try:
        # Call the method to update a unique field into the database
        response = await resp.get_query_alter_product_value("Galaxy S500","name_product","G S55")
        return {"message": f"{response}"}  # Return a success message
    
    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message


@router.get("/item")  # Define a GET endpoint for retrieving the last inserted item
async def lastst_id(): 
    # Call the method to get the last inserted item's details
    response = await resp.get_query_lest_id()
    values = [(key, value) for key, value in response.items()]  # Prepare a list of tuples with key-value pairs
    try:
        return {'item': f'Last inserted in stock {values}'}  # Return the details of the last inserted item
    
    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message
