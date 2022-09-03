from generator import generator
from end_devices import end_device, switch


class router:
    def __init__(self, port):
        self.port = port
        self.mac_table = {}
        self.ip_table = {}
        self.connected_devices = []
        self.arp_table = {}
        self.nid_table = []
        self.subnet_table = []
        self.static_routing_table = []
        self.dynamic_routing_table = []

    # def arp(self):
    #     for obj in self.connected_devices:
    #         if str(type(obj[0])) == "<class 'end_devices.end_device'>":
    #             self.arp_cache[obj[0].ip_table[obj[1]]] = obj[0].mac_table[obj[1]]

    def configure_port(self):

        gen = generator()
        for i in range(self.port):
            nid = input("Enter the NID for port no : " + str(i) + " : ")
            subnet = int(input("Enter the subnet value : "))
            self.nid_table.append(nid)
            self.subnet_table.append(subnet)
            self.mac_table[i] = gen.rand_mac()
            self.ip_table[i] = gen.ip_add(nid, subnet)

    def dynamic_routing(self):
        for i in range(self.port):
            st = "    DC    "
            self.dynamic_routing_table.append([self.nid_table[i], self.subnet_table[i], st , 0])
        self.dynamic_routing_table = sorted(self.dynamic_routing_table, key=lambda x: x[1],reverse=True)

    def table_printing(self):

        print("\t\t  __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __  __ ____ __ __ __ __ __ ")
        print("\t\t |                                               ROUTING TABLE                                         |")
        print("\t\t | __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __  __ ___ __ __ __ __ __|")
        print("\t\t |\t\tDestination\t\t\t:\t\tsubnet\t\t\t:\t\tNext hop\t\t\t:\t\tHops           |")
        print("\t\t | __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __  __ ___ __ __ __ __ __|")
        for lst in self.dynamic_routing_table:
            en1 = lst[0]
            if len(en1) < 15:
                en1 += " " * (15 - len(en1))
            en2 = lst[2]
            if len(en2) < 15:
                en2 += " " * (15 - len(en1))
            print("\t\t |\t\t"+en1+"\t\t:\t\t"+str(lst[1])+"\t\t\t\t:\t\t"+en2+"\t\t:\t\t"+str(abs(lst[3]))+"              |")
            # print("|\t"+en1+"\t:\t  "+str(lst[1])+"\t:\t"+en2+"\t:\t  "+str(abs(lst[3]))+"\t    |")
            print("\t\t | __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __  __ ___ __ __ __ __ __|")


    def connecting_port(self, prt):
        print("connecting port in current generated router : ")
        for i in range(prt):
            print("In router")
            print("Connecting port : " + str(i))
            choice = int(input("Enter the device to add : "))
            if choice == 1:
                print("Adding a router...................")
                n = int(input("Enter no of ports: "))
                obj = router(n)
                print("Configuring the ports of router: ")
                obj.configure_port()
                obj.connecting_port(n - 1)
                self.connected_devices.append([obj, 0])
            elif choice == 2:
                print("Adding a switch...................")
                n = int(input("Enter no of ports: "))
                obj = switch(n)
                obj.connecting_port(n - 1)
                self.connected_devices.append([obj, 0])
            elif choice == 3:
                print("Adding the end device..............")
                nd = input("Enter NID: ")
                sub = int(input("Enter the subnet: "))
                obj = end_device(nd, sub)
                self.connected_devices.append([obj, 0])
        print("current router configured, switching to next")

    def print_mac_ip(self):
        print("\t\tPort No.\t\t:\t\tMAC ADDRESS\t\t:\t\tIP ADDRESS")
        for i in range(self.port):
            print("\t\t\t" + str(i) + "\t\t\t:\t" + self.mac_table[i] + "\t:\t\t" + self.ip_table[i])





# dev= router(5)
# dev.configure_port()
# dev.print_mac_ip()
