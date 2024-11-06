from src.Configs.Config import Configure
from datetime import datetime
from Log.Log import LoggerSetup
import os, sys
import asyncio

# Adjusting system path to include the parent directory for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ColletionRepository:
    
    def __init__(self):
        # Initializes a connection to the MongoDB collection and sets up logging
        self.conect = self._get_collection()  # Will hold the MongoDB collection object
        self.last_client = None  # Holds the result of the last query
        self.__log = LoggerSetup(
            fr'{os.getcwd()}\Logs',
            'Log_Query.log',
            'Query Logger'
        )
        # Set the logger to ignore warnings from pymongo
        self.__log.ignor('pymongo', 'WARNING')

    def _get_connection(self) -> list:
        try:
            # Establishes connection to the database
            configure = Configure()
            self._db = configure.data_base()  # Retrieves the database configuration
            return self._db  # Returns the database object
        except Exception as e:
            # Logs any connection errors
            self.__log.errorMessage(e, 'ERROR')

    def _get_collection(self) -> list:
        try:
            self._db = self._get_connection()  # Get the database connection
            # Loads the collection name from the configuration file
            self._configure = Configure()
            self._configure = self._configure.read_json()
            self._collection_name = self._configure['COLLECTION']  # Gets collection name
            self.collection = self._db[self._collection_name]  # Retrieves the collection from the database
            
            return self.collection  # Returns the collection object

        except Exception as e:
            # Logs any errors while retrieving the collection
            self.__log.errorMessage(e, 'ERROR')

    async def query_last_id(self) -> list[list, str, int]:
        # Queries the last document by stock_id in descending order
        try:
            self.last_client = await self.collection.find_one(sort=[("stock_id", -1)])  # Finds the last stock_id
            print("self.last_client:", self.last_client)  # Debugging output
            return self.last_client  # Returns the last client document
        except Exception as e:
            # Logs any errors during the query
            self.__log.errorMessage(e, 'ERROR')

    async def query_consult_itens_product(self, product_name: str = None) -> dict[int, str]:
        """ 
        Returns the quantity of a specific product in the database.
        If the product exists, returns code: 200 and its information.
        If not found, returns code 403 with a description.
        """
        self.select = {"product.product_name": product_name}  # Set the query filter
        try:
            result = self.collection.find(self.select)  # Finds documents matching the filter
            if result:
                # Iterates over results asynchronously
                async for doc in result:
                    self.return_query_product = doc  # Stores the found document
                    self.qtd = doc["product"][0]["qtd"]  # Gets the quantity

                return {"code": 200, "qtd_itens": int(self.qtd), "product_query": self.return_query_product}
            
        except Exception as e:
            # Logs errors and returns an error response
            self.__log.errorMessage(f'code: 403 {e}', 'ERROR')
            return {"code": 403, "qtd_itens": None, "description": "Not found criteria for search product", "parameter_name": f"{product_name}"}
    
    async def insert_document(self, name_product: str, qtd_product: int, price_product: float, product_type: str) -> dict[int, str]:
        try:
            # Checks if the product already exists
            self.valida = await self.query_consult_itens_product(name_product)
            
            if self.valida["code"] != 200: 
                # Prepare to insert the new product into the database
                self.name_product: str = name_product
                self.qtd_product: int = qtd_product
                self.price_product: float = price_product
                self.data_criation: datetime = datetime.now()
                self.product_type: str = product_type
                self.product_soldout: int = 0
                self.data_modification = None
                self.last_client: int = await self.query_last_id()
                if self.last_client is None:
                    self.new_id = 1  # Set new ID if none exists
                else:
                    self.new_id = int(self.last_client["stock_id"]) + 1  # Increment last ID
                
                # Prepare the document to be inserted
                self.document = {
                    "stock_id": self.new_id,
                    "product": [{
                        "product_name": self.name_product,
                        "qtd": self.qtd_product,
                        "price_product": self.price_product,
                        "product_type": self.product_type,
                        "product_soldout": self.product_soldout
                    }],
                    "data_creation": self.data_criation,
                    "data_modification": self.data_modification
                }
                
                try:
                    # Inserts the document into the collection
                    await self.collection.insert_one(self.document)
                    return {"code": 200, "status": "Product inserted successfully"}
                except Exception as e: 
                    # Logs any insertion errors
                    self.__log.errorMessage(f'code 400 {e}', 'ERROR')
                    return {"code": 400, "description": e}
            else:
                return {"code": 403, "status": "This product already exists in the database"}
                
        except Exception as e:
            # Logs unexpected errors
            self.__log.errorMessage(f'code: 500 {e}', 'ERROR')
            return {"code": 500, "status": "An unexpected error occurred"}

    async def buy_item(self, target_product: str, qtd_itens: int) -> dict[int, str]: 
        # Attempts to buy a specified quantity of a product
        response_consult_itens = await self.query_consult_itens_product(target_product)
        print(response_consult_itens)  # Debugging output

        if response_consult_itens["code"] == 200:
            qtd_db = response_consult_itens["qtd_itens"]  # Quantity available in database
            self.document = response_consult_itens["product_query"]  # Document of the queried product

            self.__qtd_itens_user = qtd_itens  # User's requested quantity
            if self.__qtd_itens_user > qtd_db:
                return {
                    "code": "300",
                    "description": f"Desired quantity exceeds available stock. Product: {target_product} has a maximum quantity of: {qtd_db}"
                }
            else: 
                # Proceed to update the quantity of the product
                qtd_db -= self.__qtd_itens_user  # Update quantity in stock
                self.__id = self.document["stock_id"]  # Get product ID
                self.__product_name = self.document["product"][0]['product_name']
                self.__price_product = self.document["product"][0]['price_product']
                self.__product_type = self.document["product"][0]['product_type']
                self.__product_soldout = 1  # Update sold-out status
                self.__data_creation = self.document["data_creation"]

                # Prepare update document
                self.update_product = {
                    "$set": {
                        "product": [{
                            "product_name": self.__product_name,
                            "qtd": qtd_db,
                            "price_product": self.__price_product,
                            "product_type": self.__product_type,
                            "product_soldout": self.__product_soldout, 
                        }],
                        "data_creation": self.__data_creation,
                        "data_modification": datetime.now()
                    }
                }
                self.__filter = {"stock_id": self.__id}  # Filter for updating the document
                
                # Update the document in the collection
                result = await self.collection.update_one(self.__filter, self.update_product)
                
                if result.matched_count > 0:
                    print(f"{result.modified_count} document(s) updated.")
                    return {
                        "code": 200, 
                        "bought_item": [{
                            "product_name": self.__product_name,
                            "qtd": qtd_db,
                            "price_product": self.__price_product,
                            "product_type": self.__product_type,
                            "product_soldout": self.__product_soldout,
                        }],
                        "data_creation": self.__data_creation,
                        "data_modification": datetime.now()
                    }
                else:
                    return {"code": 403, "description": "Not found criteria for search product", "parameter_name": f"{target_product}"}
                 
            return result  # Returns result of update operation
        else:
            return response_consult_itens  # Return the response from product query

    async def delete_product(self, id: int, product: str = None):
        try:
            self.__id = id
            self.__product = product
            self.select = {}
            if self.__product is not None:
                self.select = {"product.product_name": self.__product}
            else: 
                self.select = {"stock_id": self.__id}  # Default selection by stock ID
            result = await self.collection.delete_one(self.select)  # Delete operation

            if result.deleted_count > 0:
                print(f"Product deleted successfully with ID: {self.__id}")
                return {"code": 200, "status": f"Product deleted successfully with ID: {self.__id}"}
            else:
                return {"code": 403, "description": f"Product not found with sucess", "id": f"{self.__id}"}
        
        except Exception as e:
            self.__log.errorMessage(f'code: 500 {e}', 'ERROR')  # Log any errors
            return {"code": 500, "status": "An unexpected error occurred"}

    async def alter_product_value(self,target_product:str,field:str, value:str) -> dict:
        """This method alter the field as name_product, qtd, price, type, soldout"""
        response_consult_itens = await self.query_consult_itens_product(target_product)
        if response_consult_itens["code"] == 200:
            self.document = response_consult_itens["product_query"]
            self.__id = self.document["stock_id"]
            self.__product_name = self.document["product"][0]['product_name']
            self.__price_product = self.document["product"][0]['price_product']
            self.__product_type = self.document["product"][0]['product_type']
            self.__product_soldout = self.document["product"][0]['product_soldout']
            self.__data_creation = self.document["data_creation"]
            self.__qtd = self.document["product"][0]["qtd"]

            self.update_product = {"$set": {"product": [{"product_name": self.__product_name,
                                                        "qtd":self.__qtd,
                                                        "price_product": self.__price_product,
                                                        "product_type": self.__product_type,
                                                        "product_soldout": self.__product_soldout #AFTER VALID THIS CAMP
                                                        }],
                                                    "data_creation":self.__data_creation,
                                                    "data_modification": datetime.now()
                                                        }}
            self.__filter = {"stock_id": self.__id}

            #Define field agreed with value 
            match field:
                case "name_product": self.update_product["$set"]["product"][0]["product_name"] = value
                case "qtd": self.update_product["$set"]["product"][0]["qtd"] = value
                case "price_product": self.update_product["$set"]["product"][0]["price_product"] = value
                case "product_type": self.update_product["$set"]["product"][0]["product_type"] = value
                case "product_soldout": self.update_product["$set"]["product"][0]["product_soldout"] = value
            print(self.update_product)
            result = await self.collection.update_one(self.__filter,self.update_product) #update into database

            if result.matched_count > 0:
                print(f"{result.modified_count} documento(s) atualizado(s).")
                return {"code": 200, "description":" update product"}
            else:
                return {"code":403, "description": "Not found criteries for search product","parameter_name": f"{target_product},{field},{value}"}