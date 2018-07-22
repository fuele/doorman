
class Packet:
    """
    Interesting information in a sniffed packet
    """

    def __init__(self):
        self.src_mac = None 
        self.dst_mac = None
        self.time = None
