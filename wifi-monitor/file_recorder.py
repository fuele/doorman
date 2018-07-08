import packet
import logging
import os

class File_Recorder:
    """
    Records sniffer activity to a file on the hard drive
    """

    def __init__ (self):
        class_name=os.path.basename(__name__)
        #self.client_file = open('clients.txt','w')
        self.logger = logging.getLogger('wifi-monitor' + '.' + class_name)
        self.clients = dict() 
    #end constructor



    def add_client(self, client_packet):
        
        if(client_packet.src_mac not in self.clients):
            self.logger.debug("Found unique client " + client_packet.src_mac + ".")
            self.clients[client_packet.src_mac]= client_packet
            self.update_client_file()
        #end if

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
        pass
    #end function

#end class
