import packet
import logging
import os
import datetime
import pymongo
import configparser
import mongo_dao

class Mongo_Writer:
    """
    Writes client activity to a mongo db
    """

    def __init__(self,dao):
        class_name = os.path.basename(__name__)
        self.logger = logging.getLogger('wifi-monitor' + '.' + class_name)
        self.dao = dao

    #end function
 
    def write(self,client_packet):
        """
        Writes the packet information to the client database
        """
        self.logger.debug("Writing packet to DB." + client_packet.src_mac)

        self.dao.insert('currentClients',{'mac':client_packet.src_mac, 'time':client_packet.timestamp})
        self.logger.debug('finished adding document to  db')
        

    #end function

    def drop_current_clients(self):
        """
        Removes all documents in the current clients collection
        """
        self.logger.debug('droping current clients') 
        self.dao.drop_collection('currentClients')
        self.logger.debug('done droping clients')

    #end function
        



#end class
