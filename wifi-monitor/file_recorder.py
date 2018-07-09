import packet
import logging
import os
import datetime

class File_Recorder:
    """
    Records sniffer activity to a file on the hard drive
    """

    def __init__ (self):
        class_name=os.path.basename(__name__)
        self.logger = logging.getLogger('wifi-monitor' + '.' + class_name)
        self.clients = dict()
        self.client_ttl_sec = 900 
    #end constructor



    def add_client(self, client_packet):

        if(client_packet.src_mac not in self.clients):
            self.logger.debug("Found unique client " + client_packet.src_mac + ".")
            self.clients[client_packet.src_mac]= client_packet
            self.update_client_file()
        #end if

        self.purge_old_clients()

    #end function

    def update_client_file(self):
        """
        makes the local client file match the objects client set
        """
        
        self.logger.debug("Updating the client file to contain " + str(len(self.clients)) + " clients") 
        self.client_file = open('clients.txt','w')

        for key in self.clients:
            self.client_file.write(self.clients[key].src_mac + "\n")

        self.client_file.close()
    #end function

    def purge_old_clients(self):
        """
        Goes through the client list and removes any clients that
        haven't been seen for a while
        """

        #we cannot modify a dict while iterating through it
        clients_to_remove = set()

        for key in self.clients:
            age_in_sec = (datetime.datetime.now() - self.clients[key].timestamp).total_seconds()

            if age_in_sec > self.client_ttl_sec:
                self.logger.debug("Staging old client " + key + " for deletion")
                clients_to_remove.add(key)
            #end if
        #end for
        
        if len(clients_to_remove) > 0:
            for key in clients_to_remove:
                self.logger.debug("Attempting to delete " + key)
                del self.clients[key]
            #end for
            self.update_client_file()
        #end if

        
    #end function

#end class
