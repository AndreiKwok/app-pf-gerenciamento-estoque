import os
from src.database.Query import ColletionRepository  # Import the ColletionRepository class for database operations
from Log.Log import LoggerSetup  # Import LoggerSetup for logging messages
import asyncio  # Import asyncio for handling asynchronous operations

class Response:
    def __init__(self) -> None:
        # Initialize an instance of ColletionRepository to interact with the database
        self._collection: list = ColletionRepository()
        # Initialize the logger for this class, specifying the log file location and name
        self.__log = LoggerSetup(
            fr'{os.getcwd()}\Logs',
            'Log_Response.log',
            'Response Logger'
        )

    async def get_query_lest_id(self):
        """
        Asynchronously retrieves the last inserted ID from the collection.
        """
        try:
            self._collection._get_collection()  # Ensure the collection is accessible
            self._response = await self._collection.query_last_id()  # Fetch the last ID
            return self._response  # Return the fetched ID
        except Exception as e:
            self.__log.errorMessage(e, 'ERROR')  # Log any errors that occur

    async def get_query_consult_itens_product(self, name_item: str = None):
        """
        Asynchronously queries for items in the collection based on the provided item name.
        """
        try:
            self._response = await self._collection.query_consult_itens_product(name_item)  # Fetch items matching the name
            return self._response  # Return the fetched items
        except Exception as e:
            self.__log.errorMessage(e, 'ERROR')  # Log any errors that occur

    async def get_insert_document(self, name_product: str = None, qtd_product: int = None, 
                                  price_product: float = None, product_type: str = None):
        """
        Asynchronously inserts a new document (product) into the collection.
        """
        try:
            self._collection._get_collection()  # Ensure the collection is accessible
            
            # Check if all required values are provided before proceeding
            if not all([name_product, qtd_product, price_product, product_type]):
                return {
                    'response': 'Missing values!',
                    'code': 400, 
                    'status': 'Missing values for insertion'
                }
             
            response = await self._collection.insert_document(name_product, qtd_product, price_product, product_type)  # Insert the new product
            return response
        except Exception as e:
            self.__log.errorMessage(f'code: 500 {e}', 'ERROR')  # Log the error with a custom message
            return {"code": 500, "status": "Insertion failed", "error": str(e)}  # Return an error response

    async def get_buy_item(self, target_product: str = None, qtd_itens: int = None):
        """
        Asynchronously processes the purchase of a specified product.
        """
        # Uncomment the try-except block for error handling if needed
        self._collection._get_collection()  # Ensure the collection is accessible      
        self._response = await self._collection.buy_item(target_product, qtd_itens)  # Fetch the response from the buy_item method
        return self._response  # Return the purchase response

        # except Exception as e:
        #     self.__log.errorMessage(e, 'ERROR')  # Log any errors that occur

    async def get_query_alter_product_value(self,target_product:str = None,field:str = None, value:str | int | float = None):
        """This method alter the field as name_product, qtd, price, type, soldout you should use 
        "name_product" for alter the value of name product
        "qtd" for alter the value of quantity product
        "price_product for alter the value of price product
        "product_type" for alter the value of type product
        "product_soldout" for alter the value of soldout product"""
        self._collection._get_collection()  # Ensure the collection is accessible      
        self._response = await self._collection.alter_product_value(target_product, field, value)  # Fetch the response from the alter method
        return self._response  # Return the  response
    
    async def delete_product(self, id: int = None, product: str = None):
        """ This method realize the delete of items in db, you should use id or the product name to delete """
        self._collection._get_collection()  # Ensure the collection is accessible      
        self._response = await self._collection.delete_product(id, product)  # Fetch the response from the delete item method
        return self._response  # Return the  response
    
   
        