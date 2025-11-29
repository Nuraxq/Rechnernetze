import struct
from collections import defaultdict, deque

class Database:
    """
    A class to manage and store data for multiple unique IDs (UIDs), 
    tracking sequence numbers, temperatures, humidities, and wind speeds.
    """

    # Keeps track of UIDs already entered into the database
    __present_uids = set()

    def __getNewDict(self):
        """
        Internal method to create a new empty data dictionary for a UID.
        
        Returns:
            dict: A dictionary with initialized keys for last sequence number 
                  and deques for temperatures, humidities, and wind speeds.
        """
        return {
            "last_sequence_number": None,
            "temperatures": deque(maxlen=100),
            "humidities": deque(maxlen=100),
            "wind_speeds": deque(maxlen=100)
        }

    def __init__(self):
        """
        Constructor initializes an empty data collection for storing UID-specific data.
        """
        try:
            self.data_collection = defaultdict()
        except:
            raise

    def add_new_uid(self, uid):
        """
        Adds a new UID to the database and initializes its associated data structure.
        
        Args:
            uid (str): The unique identifier for the new entry.
        """
        try:
            self.__present_uids.add(uid)
            self.data_collection[uid] = self.__getNewDict()
        except:
            raise

    def add_data(self, uid, temperature, humidity, wind_speed):
        """
        Adds a single set of temperature, humidity, and wind speed values for a given UID.
        
        Args:
            uid (str): The unique identifier for the entry.
            temperature (float): The temperature value to add.
            humidity (float): The humidity value to add.
            wind_speed (float): The wind speed value to add.
        """
        try:
            self.data_collection[uid]["temperatures"].append(temperature)
            self.data_collection[uid]["humidities"].append(humidity)
            self.data_collection[uid]["wind_speeds"].append(wind_speed)
        except:
            raise

    def set_last_sequence_number(self, uid, sequence_number):
        """
        Updates the last sequence number for a given UID.
        
        Args:
            uid (str): The unique identifier for the entry.
            sequence_number (int): The sequence number to set.
        """
        try:
            self.data_collection[uid]["last_sequence_number"] = sequence_number
        except:
            raise

    def get_present_uids(self):
        """
        Returns the set of all UIDs currently in the database.
        
        Returns:
            set: A set of UIDs present in the database.
        """
        try:
            return self.__present_uids
        except:
            raise

    def getData(self, uid, key):
        """
        Retrieves all saved values under a given key for a specified UID.
        
        Args:
            uid (str): The unique identifier for the entry.
            key (str): The key to retrieve data for (e.g., "temperatures").
        
        Returns:
            Any: The data associated with the specified key for the UID.
        
        Raises:
            ValueError: If the key is invalid or not in the data dictionary.
        """
        try:
            if key not in self.__getNewDict().keys():
                raise ValueError(f"Invalid key: {key}")
            return self.data_collection[uid][key]
        except:
            raise
