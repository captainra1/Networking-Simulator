from generator import generator
import router
import random

# from router import router
class end_device:
    def __init__(self, nid, subnet):
        self.nid = nid
        self.subnet = subnet
        self.gen = generator()
        self.mac_table = {}
        self.ip_table = {}
        self.arp_table = {}
        self.mac_table[0] = self.gen.rand_mac()
        self.ip_table[0] = self.gen.ip_add(self.nid, self.subnet)
        self.gateway = ""
        self.data = ""
        self.process = {}

    def receive(self,message):
        if message.destination_mac == self.mac_table[0] or message.destination_ip == self.ip_table[0]:
            self.data = message.data
            return True
        else:
            return False
    def process_port(self):
        self.process["instagram"] = 443
        self.process["gmail"] = 993
        self.process["newprc"] = random.randrange(100)




class switch:
    def __init__(self, port):
        self.port = port
        self.connected_devices = []
        self.switch_table = {}

    def connecting_port(self, prt):
        print("connecting port in current generated switch : ")
        for i in range(prt):
            print("In switch:")
            print("Connecting port : " + str(i))
            choice = int(input("Enter the device to add : "))
            if choice == 1:
                print("Adding a router...................")
                n = int(input("Enter no of ports: "))
                obj = router.router(n)
                print("Configuring the ports of router: ")
                obj.configure_port()
                obj.connecting_port(prt - 1)
                self.connected_devices.append([obj, 0])
            elif choice == 2:
                print("Adding a switch...................")
                n = int(input("Enter no of ports: "))
                obj = switch(n)
                obj.connecting_port(prt - 1)
                self.connected_devices.append([obj, 0])
            elif choice == 3:
                print("Adding the end device..............")
                nd = input("Enter NID: ")
                sub = int(input("Enter the subnet: "))
                obj = end_device(nd, sub)
                self.connected_devices.append([obj, 0])
        print("current switch configured, switching to next")

    def switching(self):
        for i, device in enumerate(self.connected_devices):
            if str(type(device[0])) != "<class 'end_devices.switch'>":
                self.switch_table[device[0].mac_table[device[1]]] = i

    def print_mac(self):
        print(" __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ ")
        print("|                                Switch Table                                 |")
        print("|__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __|")
        print("|\t\tMAC ADDRESS\t\t\t\t\t:            PORT NO.\t\t\t\t\t  |")
        print("|__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __|")
        for key in self.switch_table.keys():
            print("|\t" + str(key)  + "\t\t\t\t:\t\t\t  " + str(self.switch_table[key]) + "\t\t\t\t\t\t  |")
            # print("|\t" + str(key) + "\t\t:\t\t\t" + str(self.switch_table[key])+"\t      |")
            print("|__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __|")

# dev= end_device("123.25.116.0",20)
# print(dev.ip[0])
# print(dev.mac[0])

# dev.configure_port()
# dev.print_mac()
