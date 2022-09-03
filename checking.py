import datetime
import time
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
        print(str(datetime.datetime.now())+"\t\t:\t\t" + frame + "\t\t:\t\tAck received.............")
        time.sleep(1.5)
        win += 1
        if win % 3 == 0:
            print("\n")
            print("sliding the window:")
            print("\n")
            time.sleep(3)

go_back_n()