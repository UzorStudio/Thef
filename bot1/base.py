
import pymongo
from bson import ObjectId



def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

class Base:
    def __init__(self, classterMongo):
        self.classterMongo = classterMongo
        self.classter = pymongo.MongoClient(self.classterMongo)

    def addAdress(self,adress):
        db = self.classter["Thef"]
        Adress = db["Adress"]
        post = {"adr":adress,"private_key":'',"fuller":False,"balance":0}
        Adress.insert_one(post)

    def addWallet(self,adress,private_key,balance):
        db = self.classter["Thef"]
        Adress = db["Adress"]

        post = {"adr": adress, "private_key": private_key, "fuller": True, "balance": balance}
        Adress.insert_one(post)

    def getByAddres(self,adress,private_key):
        db = self.classter["Thef"]
        Adress = db["Adress"]
        adr = Adress.find_one({"adr":adress})
        if adr is None:
            return 0
        else:
            Adress.update_one({"adr":adress},{"$set":{"private_key":private_key,"fuller":True}})
            return 1

    def getAdressCount(self):
        db = self.classter["Thef"]
        Adress = db["Adress"]

        st = Adress.find({"fuller": True})
        dr = []

        for s in st:
            dr.append(s)

        return len(dr)