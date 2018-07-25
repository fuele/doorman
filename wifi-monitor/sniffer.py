#!/usr/bin/python3

"""

This scans for all wifi traffic that it can find and then outputs the client information
to the disk

"""
from datetime import datetime
import logging
from scapy.all import *
import packet
import sys


class Sniffer:
    """
    A wireless network monitor that looks for clients and available networks
    """



    def __init__(self, writer):
        class_name=os.path.basename(__name__)
        self.logger = logging.getLogger('wifi-monitor' + '.'+class_name)
        self.writer=writer
        self.running=False
        self.router_mac = '94:10:3e:75:20:96'
        self.capture_filter='ether dst host ' + self.router_mac
    #end constructor


    def process_packet(self, scappy_packet):
        """
        Creates a custom packet object and sends it to further processing
        """


        #we are only interested in sniffing wifi packets
        if scappy_packet.haslayer(Dot11):
       
            #The 802.11 protocol occaionslly calls to send packets out to clear the air from contention
            #and will send packets to the access point with no source MAC. Since we are only interested
            #in tracking clients and AP beacons, we want to ignore these packets
            if(scappy_packet.addr2 is not None):
                p = packet.Packet()
                p.src_mac = scappy_packet.addr2
                p.dst_mac = scappy_packet.addr1
                p.time = datetime.utcnow()
            
                if(p.dst_mac == self.router_mac ):
                    self.logger.debug('found an interesting packet')
                    self.write(p)

            #get SSID from beacons
            #if(packet.type == 0 and packet.subtype == 8 and packet.info is not b''):
            #    print("SSID: " +packet.info.decode('ascii'))
            #    print("Router: " + packet.addr2)
        else:
            print('Not a dot11 packet')
        #end if dot11 packet
    #end process_packet

    def write(self, p):
        """
        Records a list of all clients
        """
        self.writer.write(p)

    #end log_client

    def start(self):
        """
        begins to sniff all traffic off the air.
        """
        self.logger.info('starting wireless sniffer')
        self.logger.info('Using capture filter: ' + self.capture_filter)
        self.running = True

        while self.running:
            try:
                sniff(filter=self.capture_filter, iface="wlan0", prn=self.process_packet, store=0, stop_filter=self.should_stop )
            except Exception as e:
                self.logger.error('Unhandled exception in sniff function')
                self.logger.error(repr(e))
            #end try catch
        #end while true

        self.logger.info('shut down wireless sniffer')
    #end start

    def stop(self):
        """
        tells the sniffer to stop listening for packets
        """
        self.logger.info('stopping sniffer')
        self.running = False
        sys.exit()
    #end function


    def should_stop(self,p):
        """
        Tells the sniffer whether it should keep running or not
        """
        return not self.running
    #end function

#end class


#def main():
#    script_name=os.path.basename(__file__)
#    logger = logging.getLogger(script_name)
    
    
#    logger.info('Starting program')

#    logger.info('Begin sniffing')
    #store=0 tells it not to cache packets in ram, but discard them after use
#    sniff(iface="wlan0", prn=process_packet, store=0)

#    logger.info('Exiting program')


#if (__name__ == "__main__"):
#    main()


