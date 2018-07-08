import packet
import logging
import os

class File_Recorder:
    """
    Records sniffer activity to a file on the hard drive
    """


    def __init__ (self):
        class_name=os.path.basename(__name__)
        self.client_file = open('clients.txt','w')
        self.logger = logging.getLogger('wifi-monitor' + '.' + class_name)
        self.clients = dict() 



    def add_client(self, client_packet):
        
        if(client_packet.src_mac not in self.clients):
            self.logger.debug("Found unique client " + client_packet.src_mac + ".")
            self.clients[client_packet.src_mac]= client_packet
            self.client_file.write(client_packet.src_mac + "\n")



#end class
