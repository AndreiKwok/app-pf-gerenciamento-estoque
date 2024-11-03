from motor.motor_asyncio import AsyncIOMotorClient
import json
import os

class Configure:

    def read_json(self) -> dict:
        # Reads configuration from a JSON file
        self._current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
        self._json_path = os.path.join(self._current_dir, 'Mongo_config.json')  # Construct the path to the JSON config file
        with open(self._json_path, 'r') as file:  # Open the JSON file for reading
            self._config_data = json.load(file)  # Load the JSON data into a dictionary
        return self._config_data  # Return the configuration data

    def data_base(self) -> list:
        # Establishes MongoDB connection using the URI from the JSON config
        self._config = self.read_json()  # Read the JSON configuration
        self._client = AsyncIOMotorClient(self._config['URI'])  # Create an AsyncIOMotorClient using the URI from the config
        self._client = self._client[self._config['DB_NAME']]  # Access the specified database using the DB_NAME from the config

        return self._client  # Return the database client
