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
        response = await resp.get_query_consult_itens_product('Galaxy S24 Ultra')
        print(response)
        if int(response["code"]) == 200:
            stock_id = response["product_query"]["stock_id"]
            product = response["product_query"]["product"][0]
            name_product = product["product_name"]
            qtd_prod = product["qtd"]
            price_prod = product["price_product"]
            type_prod = product["product_type"]

            return {'stock_id': f'{stock_id}','product_name':f'{name_product}', 'qtd_product':f'{qtd_prod}','price_product':f'{price_prod}','type_product':f'{type_prod}'}  # Return the item details as a response
        else: 
            code = response['code']
            description = response['description']
            parameter_name = response['parameter_name']
            
            
            return {f'code': f'{code}','description': f'{description}', 'name_error': {parameter_name}}
    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message

@router.get("/items/buy_item")  # Define a GET endpoint for purchasing an item
async def buy(): 
    try:
        # Call the method to buy an item
        response = await resp.get_buy_item("Galaxy S24 Ultra", 20)
        print(response)
        if int(response["code"]) == 200:
            stock_id = response["bought_item"][0]["stock_id"]
            product = response["bought_item"][0]
            name_product = product["product_name"]
            qtd_prod = product["qtd"]
            price_prod = product["price_product"]
            type_prod = product["product_type"]

            return {'status_product': 'Item bought','stock_id': f'{stock_id}','product_name':f'{name_product}', 'qtd_product':f'{qtd_prod}','price_product':f'{price_prod}','type_product':f'{type_prod}'}  # Return the item details as a response
        else: 
            code = response['code']
            description = response['description']
           
            
            return {f'code': f'{code}','description': f'{description}'}  # Return a success message with the bought item details

    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message

@router.get("/items/insert_item")  # Define a GET endpoint for inserting a new item
async def insert(): 
    try:
        # Call the method to insert a new item into the database
        response = await resp.get_insert_document('Iphone 15', 10, 5.600, 'Celular')
        return {"message": f"{response}"}  # Return a success message
    
    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message

@router.get("/item/alter_fild_item")  # Define a GET endpoint for inserting a new item
async def insert_unique_value(): 
    try:
        # Call the method to update a unique field into the database
        response = await resp.get_query_alter_product_value("Iphone 16 Pro Max","product_type", "IOS")
        return {"message": f"{response}"}  # Return a success message
    
    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message

@router.get("/item/delete_item")  # Define a GET endpoint for inserting a new item
async def delete_product(): 
    id = []
    try:
        # response = list(map(lambda x: await resp.delete_product(x), range(10)))
        # Call the method to delete product into the database
        #for i in range(2):
        response = await resp.delete_product(1)
        resp_id = response["id"]
        id.append(str(resp_id))
        return {"message": f"{response["description"]}, id(s): {id}"}  # Return a success message
    
    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message


@router.get("/item")  # Define a GET endpoint for retrieving the last inserted item
async def last_id(): 
    # Call the method to get the last inserted item's details
    response = await resp.get_query_last_id()
    values = [(key, value) for key, value in response.items()]  # Prepare a list of tuples with key-value pairs
    try:
        return {'item': f'Last inserted in stock {values}'}  # Return the details of the last inserted item
    
    except Exception as e:  # Catch any exception that occurs
        log.errorMessage(e, 'ERROR')  # Log the error message
        return {"ERROR": f"An error occurred while processing the request: {str(e)}"}  # Return an error message
