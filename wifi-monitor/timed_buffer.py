
import logging
from datetime import datetime
import packet
import os

class Timed_Buffer:
    """
    Keeps a collection of client packets from unique sources
    Flushes the collection after a set number of seconds to a 
    designated writer.
    This is useful if we don't want to record every packet recieved
    by the sniffer
    """

    def __init__(self, writer, ttl):
        class_name=os.path.basename(__name__)
        self.logger = logging.getLogger('wifi-monitor' + '.' + class_name)
        self.logger.debug('created Timed_Buffer')
        self.ttl = ttl
        self.writer = writer
        self.flush()
    #end constructor

    def add_client_packet(self, client_packet):
        """
        If the buffer does not have a packet from this client's
        MAC then it will add it to the collection.
        If the buffer already has one, then the new packet is discarded
        Flushes the buffer to the writer if the elapsed time has past 
        since the last flush.
        """
       
        self.logger.debug('Receiving request to add packet for ' + client_packet.src_mac + '.')

        if client_packet.src_mac not in self.clients:
            self.logger.debug("Found unique client " + client_packet.src_mac + ".")
            self.clients[client_packet.src_mac] = client_packet
            self.writer.write(client_packet)

        if self.should_flush():
            self.flush()

    #end function

    def should_flush(self):
        """
        Checks if the buffer is old enough and it's time to flush the buffer
        to the writer
        """
        now=datetime.utcnow()

        delta=now - self.last_flush_time

        if delta.seconds > self.ttl:
            return True
        else:
            return False



    #end function


    def flush(self):
        """
        Sends all the client packets in the buffer to the designated writer
        and resets the timer.
        """

        self.last_flush_time = datetime.utcnow()
        self.logger.debug('flushing buffer')

        #remove all the old entries in the db so we only show the ones that have
        #appeared since the last flush
        self.writer.drop_current_clients()        


        #for key in self.clients:
        #    self.logger.debug('sending something to writer')
        #    self.writer.write(self.clients[key])

        self.clients = dict()
        self.logger.debug('done flushing buffer')

    #end function

            



#end class




