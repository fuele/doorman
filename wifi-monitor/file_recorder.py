import packet
import logging
import os

class File_Recorder:
    """
    Records sniffer activity to a file on the hard drive
    """


    def __init__ (self):
        class_name=os.path.basename(__name__)
        self.client_file = open('clients.txt','a')
        self.logger = logging.getLogger('wifi-monitor' + '.' + class_name)



    def add_client(self, client_packet):
        self.logger.debug("Writing client " + client_packet.src_mac + " to file")
        self.client_file.write(client_packet.src_mac + "\n")



#end class
