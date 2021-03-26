from sqlite_utils import Database

class DB:    
    
    # Initialize a Database locally
    def __init__(self, database_name, table_name):
        self.db         = Database(f"{database_name}.db")
        self.table_name = table_name
    
    # To insert the data into the table in a Database
    def insert_data(self, data):
        """
        Function to insert the data into the database that is initialized when the class is called.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            **data (dict):** Data that is to be inserted in the database, it should follow the schema defined below
            
                - Region: region
                - AZ: az
                - InstanceType: instanceType
                - Product: product
                - Price: price
                - TimeStamp: timestamp
                

        Returns:
            **None**

        """
        self.db[self.table_name].insert(data)