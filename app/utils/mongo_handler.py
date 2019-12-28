import logging
import pymongo

from config import Config

logging.basicConfig(level=logging.DEBUG)
_MONGOCLIENT = pymongo.MongoClient(Config.MONGOCLIENT)

class MongoHandler(object):

    def __init__(self,db,collection):
        self.db = db
        self.collection = collection
        self.mdb = _MONGOCLIENT[self.db]
        self.mcollection = self.mdb[self.collection]

    def insertIntoMongo(self,data):
        '''
        :param db: str -> name of mongo db (e.g. bestsellers)
        :param collection: str -> name of collection in db (e.g. outdoors)
        :param data: dict
        :return: None
        '''
        filter = {"start_date": {"$gte": data['start_date']}, "end_date": {"$lte": data['end_date']}}
        if self.mcollection.count_documents(filter):
            logging.info(f"data already exists for {self.collection} on start_date {data['start_date']}")
        else:
            self.mcollection.insert_one(data)
            logging.info('data loaded to : {db}|{col}'.format(db=self.db,col=self.collection))

    def getFromMongoByDateRange(self,start_date,end_date):
        d = {}
        filter = {"start_date":{"$gte":start_date},"end_date":{"$lte":end_date}}
        if self.mcollection.count_documents(filter):
            docs = self.mcollection.find(filter)
            for doc in docs:
                d[doc['start_date']] = doc['html']
            return d

def main():
    m = MongoHandler('futures','sp500')
    d = m.getFromMongoByDateRange('2017-12-01','2019-12-31')

if __name__=="__main__":
    main()