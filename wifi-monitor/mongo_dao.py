import logging
import os
import pymongo
import configparser

class Mongo_DAO:
    """
    Data Access Object, class responsible for communicating with mongo db
    """

    CONFIG_PATH = './monitor.conf'
    DB_HEADER = 'DATABASE'

    def __init__(self):
        class_name = os.path.basename(__name__)
        self.logger = logging.getLogger('wifi-monitor' + '.' + class_name)

    #end function
 
    def get_uri(self):
       self.logger.debug('attempting to read config file at ' + self.CONFIG_PATH)
       config = configparser.ConfigParser() 
       config.read(self.CONFIG_PATH)

       user=config.get(self.DB_HEADER,'User')
       password=config.get(self.DB_HEADER,'Password')
       host=config.get(self.DB_HEADER,'Host')
       database=config.get(self.DB_HEADER,'Database')

       uri = 'mongodb://' + user + ':' + password + "@" + host + '/' + database
       return uri
   #end function


    def connect(self):
        self.logger.debug('Attempting to connect to database')
        uri = self.get_uri()
        self.client = pymongo.MongoClient(uri)
        self.db = self.client.get_default_database()
        self.logger.debug('connected to db')
    #end function

    def insert(self,collection,doc):
        """
        Adds a document to a collection
        """

        self.logger.debug('Inserting into collection ' + collection)

        col = self.db[collection]
        col.insert(doc)
        self.logger.debug('finished adding document to  db')

    #end function

    def drop_collection(self,collection):
        """
        Removes all documents in the current clients collection
        """
        self.logger.debug('droping collection ' + collection) 
        self.db.drop_collection(collection)
        self.logger.debug('done droping ' + collection)

    #end function

    def find(self, collection, query, formatting):
        """
        Performes a search in the database for the query
        """
        self.logger.debug('Entering find')
        self.logger.debug('collection' + collection + ' query ' + str(query))
        col = self.db[collection]

        cursor = col.find(query, formatting) 

        self.logger.debug('Exiting find')
        
        return cursor
    #end function

    def update_one(self, collection, query, update):
        """
        updates a single document  
        e.g.
        update_one('uniqueClients',{'_id':'fdeee'},{'nick':'bob'},false)
        upsert=true means it will insert into the collection if the query fails
        """
        self.logger.debug('updating document')
        self.logger.debug('collection' + collection + ' query ' + str(query) +' update ' + str(update))


        col = self.db[collection]

        col.update_one(query,update)

        self.logger.debug('update successful')
    #end function

#end class
