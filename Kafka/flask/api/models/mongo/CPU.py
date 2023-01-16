from api.v1 import cpu_collection

class CPU:

    def __init__(self,name):
        self.name = name

    def register(self):
        x = cpu_collection.insert_one(self.__dict__)
        return x.inserted_id

        
    @staticmethod
    def fetchAll():
        return cpu_collection.find({},{ "_id": 0})
    
    @staticmethod
    def fetch(id):
        myquery = {"_id": id}
        mydoc = cpu_collection.find(myquery)
        return mydoc



