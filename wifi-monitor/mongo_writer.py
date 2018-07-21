import packet
import logging
import os
import datetime
import pymongo
import configparser

class Mongo_Writer:
    """
    Writes client activity to a mongo db
    """

    def __init__(self):
        class_name = os.path.basename(__name__)
        self.logger = logging.getLogger('wifi-monitor' + '.' + class_name)
        uri = self.get_uri('./monitor.conf')
        self.connect(uri)

    #end function
 
    def get_uri(self,file_path):
       self.logger.debug('attempting to read config file at ' + file_path)
       config = configparser.ConfigParser() 
       config.read(file_path)

       header='DATABASE'

       user=config.get(header,'User')
       password=config.get(header,'Password')
       host=config.get(header,'Host')
       database=config.get(header,'Database')

       uri = 'mongodb://' + user + ':' + password + "@" + host + '/' + database
       return uri
   #end function


    def connect(self,uri):
        print(uri)
        self.logger.debug('Attempting to connect to database')
        self.client = pymongo.MongoClient(uri)
        self.db = self.client.get_default_database()


    def write(self,client_packet):
        """
        Writes the packet information to the client database
        """
        self.logger.debug("Writing packet to DB." + client_packet.src_mac)

        col = self.db['currentClients']
        col.insert({'mac':client_packet.src_mac, 'time':client_packet.timestamp})
        self.logger.debug('finished adding document to  db')
        

    #end function

    def drop_current_clients(self):
        """
        Removes all documents in the current clients collection
        """
        self.logger.debug('droping current clients') 
        self.db.drop_collection('currentClients')
        self.logger.debug('done droping clients')

    #end function
        



#end class
