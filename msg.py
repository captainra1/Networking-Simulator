class Message:
    def __init__(self):
        self.source_ip = ""
        self.destination_ip = ""
        self.source_mac = ""
        self.destination_mac = ""
        self.data = ""
        self.port = 0
        self.encapsulated_data = ""

    def layer2_header(self, sorc_mac, dest_mac):
        self.source_mac = sorc_mac
        self.destination_mac = dest_mac

    def layer3_header(self, sorc_ip, dest_ip):
        self.source_ip = sorc_ip
        self.destination_ip = dest_ip

    def layer4_header(self,port):
        self.port = port
    def en_data(self,data):
        self.encapsulated_data = data
    def binary_converter(self,ip):
        word = ip.split('.')
        id_bin = ""
        for i in word:
            i_bin = bin(int(i))[2:]
            dec = 8 - len(i_bin)
            str1 = '0' * dec
            id_bin += str1 + i_bin
        return id_bin

    def ip_encapsulator(self, src_ip, dest_ip):
        self.encapsulated_data = self.binary_converter(src_ip)+self.binary_converter(dest_ip)+self.encapsulated_data


    #def mac_encapsulator(self, mac1, mac2):

    def port_encapsulator(self, port):
        prt_bin =  bin(int(port))[2:]
        self.encapsulated_data = prt_bin + self.encapsulated_data
