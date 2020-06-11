"""
This file is a proof of concept script meant to explore
how to parse wireless packets with scapy.
It runs in an infinite loop and merely prints the fields we
are interested in on the screen ad infinitum
"""


from scapy.all import *


def process_packet(packet):
    """
    Print out a few interesting attributes for each packet
    """

    if packet.haslayer(Dot11):
        print(packet.summary())
        if(packet.addr1 is not None):
            print("dst:" + packet.addr1)
        if(packet.addr2 is not None):
            print("src:" + packet.addr2)

        #get SSID from beacons
        if(packet.type == 0 and packet.subtype == 8 and packet.info is not b''):
            print("SSID: " +packet.info.decode('ascii'))
            print("Router: " + packet.addr2)
    else:
        print('Not a dot11 packet')

    print('')
#end process_packet


def main():

    print("Start the sniffing!")

    #store=0 tells it not to cache packets in ram, but discard them after use
    sniff(iface="wlan0", prn=process_packet, store=0)



if (__name__ == "__main__"):
    main()


