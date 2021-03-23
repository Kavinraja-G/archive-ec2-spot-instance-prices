from sqlite_utils import Database

class DB:    
    
    # Initialize a Database locally
    def __init__(self, database_name, table_name):
        self.db         = Database(f"{database_name}.db")
        self.table_name = table_name
    
    # To insert the data into the table in a Database
    def insert_data(self, data):
        self.db[self.table_name].insert(data)