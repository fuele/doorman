
import logging
from datetime import datetime
import packet
import os
import mongo_dao
import nickname_resolver


class Unique_Client_Writer:
    """
    Just writes to a table that keeps the latest timestamp for each 
    client. This writes a lot
    """

    def __init__(self):
        class_name = os.path.basename(__name__)
        self.logger = logging.getLogger('wifi-monitor.' + class_name)
        self.logger.debug('created ' + class_name)
        self.table = 'uniqueClients'
    #end function

    def set_dao(self, dao):
        """
        Sets the object that will handle datastore connectivity
        """
        self.dao = dao
        self.nick_resolver = nickname_resolver.Nickname_Resolver(dao)
        self.__load_cache()
    #end function

    def __load_cache(self):
        """
        Reads the list of current clients from the database and
        populates an in memory cache
        """

        self.logger.debug('Loading client cache from db')

        cursor = self.dao.find(self.table,{},None)

        self.mac_cache = dict()

        for i in cursor:
            self.logger.debug('adding  mac to cache' + i['mac'])
            self.mac_cache[i['mac']] = i

        self.logger.debug('ending load clients cache')
    #end function



    def write(self,client_packet):
        """
        adds the client to the current client table if they are not there.
        If they are present, updates the timestamp
        """
        self.logger.debug('got a client with src mac ' + client_packet.src_mac)

        #check if the mac is there already
        if client_packet.src_mac in self.mac_cache:
            self.logger.debug('mac already in cache')
            self.update_client(client_packet)
        else:
            self.add_new_client(client_packet)

    #end function

    def add_new_client(self,client_packet):
        """
        Adds a new mac to teh local cache and to the datastore
        """
        self.logger.debug('adding mac ' + client_packet.src_mac + ' to cache') 

        nick = self.nick_resolver.get_nick(client_packet.src_mac)


        cache_object = {
            'mac':client_packet.src_mac,
            'nick':nick,
            'time':client_packet.time
        }
        
        self.mac_cache[client_packet.src_mac] = cache_object
        self.dao.insert(self.table,cache_object)

        self.logger.debug('Finished adding entry to db')
    #end function


    def update_client(self, client_packet):
        """
        Updates the stored information for this client in the db 
        """

        self.logger.debug('starting update client')

        cache_object = self.mac_cache[client_packet.src_mac]

        query = {'_id':cache_object['_id']}
        update = {'$set': {'time':client_packet.time}}


        self.dao.update_one(self.table, query, update)

        self.logger.debug('exiting update_client')

    #end function




#end class

