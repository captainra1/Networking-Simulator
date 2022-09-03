from router import router
from end_devices import switch
import msg
import generator
import datetime
import time

print("******************Configure the network******************")
print("Devices available:")
print("1. Router \n2. Switch\n3. End device")
print("Press:")
print("1 to add a Router\n2 to add a switch\n3 to add a End device : ")
choice = int(input())
if choice == 1:
    print("Adding a router...................")
    n = int(input("Enter no of ports: "))
    network = router(n)
    print("Configuring the ports of router: ")
    network.configure_port()
    network.connecting_port(n)
elif choice == 2:
    print("Adding a switch...................")
    n = int(input("Enter no of ports: "))
    network = switch(n)
    print("Configuring the ports of switch: ")
    network.connecting_port(n)

i = 0  # for device no global variable.
en_dev = []   # list of all the end devices

# Adding previous device
def solve(dev, port, net):
    global i
    global en_dev
    if str(type(dev[0])) == "<class 'end_devices.end_device'>":
        i += 1
        en_dev.append(dev[0])
        print("\t\t" + str(i) + "\t\t\t:\t" + dev[0].mac_table[dev[1]] + "\t:\t\t" + dev[0].ip_table[dev[1]])
        return
    else:
        dev[0].connected_devices.insert(0, [net, port])
        for p, d in enumerate(dev[0].connected_devices):
            if p!=0:
              solve(d, p, dev[0])
        return


print("\n\n")
print("\t\t**********End devices**********")
print("\tDevice No.\t\t:\t\tMAC ADDRESS\t\t:\t\tIP ADDRESS")
for port, dev in enumerate(network.connected_devices):
    solve(dev, port, network)
print("\n\n")

sn1 = 0   #for router serial no
sn2 = 0   #for switch serial no
def table_learning(device):
    global sn1, sn2
    def sol(dev, i):
        global sn1, sn2
        if i != 0:  #to avoid endless loop
            if str(type(dev[0])) == "<class 'end_devices.switch'>":
                dev[0].switching()
                sn2+=1
                print("Switch No."+str(sn2))
                dev[0].print_mac()
                print("\n\n")
                for j, d in enumerate(dev[0].connected_devices):
                    sol(d, j)
            elif str(type(dev[0])) == "<class 'router.router'>":
                dev[0].dynamic_routing()
                sn1+=1
                print("Router No." + str(sn1))
                dev[0].table_printing()
                print("\n\n")
                for j, d in enumerate(dev[0].connected_devices):
                    sol(d, j)

    if str(type(device)) == "<class 'router.router'>":
        sn1+=1
        device.dynamic_routing()
        print("Router No."+str(sn1))
        device.table_printing()
        print("\n\n")
    for k in device.connected_devices:
        sol(k, 1)


table_learning(network)

global_table = []   #global routing table
global_dict = {}    #global routing dict


def global_routing(device):   #global router table learning.
    global global_table
    global global_dict
    if str(type(device)) == "<class 'router.router'>":
        for lst in device.dynamic_routing_table:
            lt = lst.copy()
            lt.append(device)
            global_table.append(lt)
            global_dict[lt[0]] = lt
    if str(type(device)) != "<class 'end_devices.end_device'>":
        for j, dev in enumerate(device.connected_devices):
            if j != 0:
                global_routing(dev[0])


global_routing(network)
for dvc in network.connected_devices:
    global_routing(dvc[0])

# Updating routing table:
# Using RIP protocol
all_router = []  #Router with ports

def RIP1(device, seq):   #for getting the list of the router
    global all_router
    if str(type(device[0])) == "<class 'router.router'>":
        all_router.append([device[0], device[1], seq])
        for serial,lst in enumerate(device[0].connected_devices):
            if serial!=0:
                 RIP1(lst,serial)


if str(type(network)) == "<class 'router.router'>":
    all_router.append([network,0,0])
for seq,d in enumerate(network.connected_devices):
    RIP1(d,seq)
all_router2 = []  #only router
for t1 in all_router:
    all_router2.append(t1[0])


def RIP2(all_rout, all_rout1):   #to update routing table
    for i in range(len(all_rout)):
        rtr_dict = {}
        for entry in all_rout[i][0].dynamic_routing_table:
            rtr_dict[entry[0]] = entry
        for key in global_dict.keys():
            if key not in rtr_dict.keys():
                new_entry = global_dict[key].copy()
                ind = all_rout1.index(new_entry[4])
                ent = new_entry[:4]
                if(ind-i) < 0:
                    ent[3] = ind-i
                    ent[2] = all_rout[i-1][0].ip_table[all_rout[i][2]]
                elif(ind-i) > 0:
                    ent[3] = ind-i
                    ent[2] = all_rout[i+1][0].ip_table[0]
                all_rout[i][0].dynamic_routing_table.append(ent)

RIP2(all_router, all_router2)
print("Dynamically updated routing table using RIP")
for sn,rt in enumerate(all_router2):
    print("Router No:"+str(sn+1))
    rt.dynamic_routing_table = sorted(rt.dynamic_routing_table, key=lambda x: x[1],reverse=True)
    rt.table_printing()
    print("\n\n")

# Printing ARP table
def print_arp(table):
    print("\t\t  __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ ")
    print("\t\t |                                   ARP  TABLE                             |")
    print("\t\t | __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ _|")
    print("\t\t |\t\t\t\t\tIP ADDRESS\t\t\t:\t\t\tMAC ADRESS\t\t        |")
    print("\t\t | __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ _|")
    for key in table.keys():
        en = key
        if len(en) < 15:
            en += " "*(15-len(en))
        print("\t\t |\t\t\t\t\t"+en+"\t\t:\t\t"+table[key]+"\t        |")
        print("\t\t | __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ _|")


flag = True

while flag:

    # Message sending and receiving
    s = int(input("Enter the source device no:"))
    d = int(input("Enter the destination device no:"))
    #
    #
    print("Process available:")
    en_dev[s - 1].process_port()
    for prc in en_dev[s-1].process.keys():
        print(prc)
    interface = input("Enter the process name:")



    # Adding gateway
    print("\n")
    print("Learning gateway of end devices")
    print("\n")
    for rout in all_router2:
        for prt, swt in enumerate(rout.connected_devices):
            if str(type(swt[0])) == "<class 'end_devices.switch'>":
                for pc in swt[0].connected_devices:
                    if str(type(pc[0])) == "<class 'end_devices.end_device'>":
                        pc[0].gateway = rout.ip_table[prt]
                        if pc[0].ip_table[0] == en_dev[s-1].ip_table[0] :
                            src_router,port = rout,prt


    message = msg.Message()
    message.data = input("Enter the data to send:")
    message.en_data(message.data)
    print("adding layer4 header")
    message.layer4_header(en_dev[s - 1].process[interface])
    message.port_encapsulator(message.port)
    print("Encapsulated data : "+message.encapsulated_data)
    print("adding layer3 header")
    message.layer3_header(en_dev[s-1].ip_table[0], en_dev[d-1].ip_table[0])
    message.ip_encapsulator(en_dev[s-1].ip_table[0], en_dev[d-1].ip_table[0])
    print("Encapsulated data : " + message.encapsulated_data)

    #
    def message_routing(rout, message, all_router2):
        gen = generator.generator()
        for entry in rout.dynamic_routing_table:
            if gen.check_nid(message.destination_ip, entry[0], entry[1]):
                if entry[3] == 0:
                    ind = rout.nid_table.index(entry[0])
                    if message.destination_ip not in rout.arp_table.keys():
                        print("Entry not in arp table...\n performing ARP:")
                        if str(type(rout.connected_devices[ind][0])) == "<class 'end_devices.switch'>":
                            sw = rout.connected_devices[ind][0]
                            for dev in sw.connected_devices:
                                if dev[0].ip_table[dev[1]] != rout.ip_table[ind]:
                                    print("sending arp request to:" + str(type(dev[0])) + ".......")
                                    if dev[0].ip_table[0] == message.destination_ip:
                                        rout.arp_table[message.destination_ip] = dev[0].mac_table[0]
                                        print("ARP request successful.......")
                                        print("Router ARP table:")
                                        print_arp(rout.arp_table)
                                        print("\n\n")
                                        dev[0].arp_table[rout.ip_table[ind]] = rout.mac_table[ind]
                                        print("Destination device arp table:")
                                        print_arp(dev[0].arp_table)
                                        print("\n\n")
                                    else:
                                        print("IP match not found")
                    print("Adding layer2 header......")
                    message.layer2_header(rout.mac_table[ind], rout.arp_table[message.destination_ip])
                    ack = sw.connected_devices[sw.switch_table[message.destination_mac]][0].receive(message)
                    if ack:
                        print("Message received successfully.....")
                        print("Message recieved at "+interface)
                elif entry[3] < 0:
                    index = all_router2.index(rout)
                    print("Sending msg to next router......")
                    message_routing(all_router2[index - 1], message, all_router2)
                elif entry[3] > 0:
                    index = all_router2.index(rout)
                    print("Sending msg to next router......")
                    message_routing(all_router2[index + 1], message, all_router2)



    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    print("Sending data from device having ip :"+en_dev[s-1].ip_table[0])
    print("to the device having ip :"+en_dev[d-1].ip_table[0])
    # sending the data
    if en_dev[s-1].nid == en_dev[d-1].nid:
        print("Source and destination are in same network:")
        message.layer2_header(en_dev[s-1].mac_table[0], en_dev[d-1].mac_table[0])
        swt1 = src_router.connected_devices[port][0]
        ack = swt1.connected_devices[swt1.switch_table[en_dev[d-1].mac_table[0]]][0].receive(message)
        if ack:
            print("message received successfully")
            print("Message recieved at " + interface)

    else :
        print("Source and destination are in different network:")
        if en_dev[s-1].gateway not in en_dev[s-1].arp_table.keys():
            print("Entry not in arp table...\nperforming ARP:")
            # calling arp
            for pc in src_router.connected_devices[port][0].connected_devices:
                if pc[0].ip_table[0] != en_dev[s-1].ip_table[0]:
                    print("sending arp request to:"+str(type(pc[0]))+".......")
                    if str(type(pc[0])) == "<class 'end_devices.end_device'>":
                        pr = 0
                    else:
                        pr = port
                    if pc[0].ip_table[pr] == en_dev[s-1].gateway:
                        en_dev[s - 1].arp_table[en_dev[s-1].gateway] = pc[0].mac_table[port]
                        print("ARP request successful.......")
                        print("Sender device arp table:")
                        print_arp(en_dev[s - 1].arp_table)
                        print("\n\n")
                        pc[0].arp_table[en_dev[s-1].ip_table[0]] = en_dev[s-1].mac_table[0]
                        print("Router arp table:")
                        print_arp(pc[0].arp_table)
                        print("\n\n")
                    else:
                        print("IP match not found")
                # ending arp

        print("Adding layer2 header:")
        message.layer2_header(en_dev[s-1].mac_table[0], en_dev[s-1].arp_table[en_dev[s-1].gateway])
        if src_router.mac_table[port] == message.destination_mac:
            print("Router received data successfully:")
            print("Striping layer2 header")
            message.layer2_header("", "")
        message_routing(src_router, message, all_router2)


    def go_back_n():
        stream = input("Enter stream(size>4):")
        stream_list = []
        t1 = 0
        t2 = 4
        while t2 <= len(stream):
            stream_list.append(stream[t1:t2])
            t1 += 4
            t2 += 4
        sz = 3
        window_size = 3
        win = 0
        print("Window size used: 3")
        print("\t\tTime\t\t\t\t\t:\t\tframe\t\t:\t\tstatus")
        print("-------------------------------------------------------------------------------------")
        for frame in stream_list:
            print(str(datetime.datetime.now()) + "\t\t:\t\t" + frame + "\t\t:\t\tAck received.............")
            time.sleep(1.5)
            win += 1
            if win % 3 == 0:
                print("\n")
                print("sliding the window:")
                print("\n")
                time.sleep(3)
    op = input("Want to send stream(y/n):")
    print("\n\n")
    if op == "y":
       go_back_n()
    print("\n\n")
    opt = input("Want to send more data(y/n):")
    if opt == "n":
        flag = False















