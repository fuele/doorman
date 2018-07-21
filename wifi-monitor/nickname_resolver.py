import logging
import os
import pymongo
import configparser

class Nickname_Resolver:
    """
    Resolves mac addresses into their nickname
    """


    def  __init__ (self,dao):
        class_name = os.path.basename(__name__)
        self.logger = logging.getLogger('wifi-monitor.' + class_name)
        self.dao = dao
    #end function

    def get_nick(self, mac):
        self.logger.debug('starting get_nick')
        self.logger.debug('Looking for nick for ' + mac)

        cursor = self.dao.find('macNicknames',{'mac':mac},{'nick':1})
        
        if cursor.count() == 0:
            nick = 'Unknown Device: ' + mac
        else:
            self.logger.debug(cursor[0]) 
            nick = cursor[0]['nick']

        self.logger.debug('found nickname ' + nick + ' for mac ' + mac)
        return nick
        #for doc in cursor:
        #    self.logger.debug('found doc')
        #    self.logger.debug(doc)

    #end function


#end class




