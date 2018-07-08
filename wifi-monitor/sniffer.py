#!/usr/bin/python3

"""

This scans for all wifi traffic that it can find and then outputs the client information
to the disk

"""

import logging
from scapy.all import *
import packet



def create_logger():
    script_name=os.path.basename(__file__)
    logger = logging.getLogger(script_name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh = logging.FileHandler('wifi-monitor.log') 
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s]:  %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger



def process_packet(scappy_packet):
    """
    Creates a custom packet object and sends it to further processing
    """

    router_mac = '94:10:3e:75:20:96'

    #we are only interested in sniffing wifi packets
    if scappy_packet.haslayer(Dot11):
       
        #The 802.11 protocol occaionslly calls to send packets out to clear the air from contention
        #and will send packets to the access point with no source MAC. Since we are interested
        #in tracking clients, we want to ignore these packets
        if(scappy_packet.addr2 is not None):
            p = packet.Packet()
            p.src_mac = scappy_packet.addr2
            p.dst_mac = scappy_packet.addr1
            
            if(p.dst_mac == router_mac ):
                log_client(p)

        #get SSID from beacons
        #if(packet.type == 0 and packet.subtype == 8 and packet.info is not b''):
        #    print("SSID: " +packet.info.decode('ascii'))
        #    print("Router: " + packet.addr2)
    else:
        print('Not a dot11 packet')
    #end if dot11 packet
#end process_packet

def log_client(p):
    """
    Records a list of all clients
    """

    print(p.src_mac + "=>" + p.dst_mac)

#end log_client



def main():
    logger = create_logger()
    logger.info('Starting program')

    logger.info('Begin sniffing')
    #store=0 tells it not to cache packets in ram, but discard them after use
    sniff(iface="wlan0", prn=process_packet, store=0)

    logger.info('Exiting program')


if (__name__ == "__main__"):
    main()


