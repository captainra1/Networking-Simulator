from random import randrange
encode={10:'A',11:'B',12:'C',13:'D',14:'E',15:'F'}
class generator:
    def rand_mac(self):
        mac=""
        st =""
        while(len(mac)<17):
            r=randrange(16)
            if(r>9):
                st+=encode[r]
            else:
                st+=str(r)
            if(len(st)==2):
                mac+=st
                st=""
                if(len(mac)<17):
                    mac+=':'
        return mac

    def ip_add(self,nid,subnet):
        word=nid.split('.')
        nid_bin=""
        for i in word:
            i_bin = bin(int(i))[2:]
            dec = 8 - len(i_bin)
            str1 = '0' * dec
            nid_bin += str1 + i_bin
        ip_bin=nid_bin[:subnet]
        while (len(ip_bin) < 32):
            ip_bin += str(randrange(2))
        t1=0
        t2=8
        ip = ""
        while (t2 <= 32):
            ip += str(int(ip_bin[t1:t2], 2))
            ip += '.'
            t1 += 8
            t2 += 8
        return ip[:len(ip)-1]

    def check_nid(self,src_ip,dest_ip,subnet):
        word1 = src_ip.split('.')
        word2 = dest_ip.split('.')
        nid1_bin = ""
        nid2_bin = ""
        for i in word1:
            i_bin = bin(int(i))[2:]
            dec = 8 - len(i_bin)
            str1 = '0' * dec
            nid1_bin += str1 + i_bin
        id1_bin = nid1_bin[:subnet]

        for i in word2:
            i_bin = bin(int(i))[2:]
            dec = 8 - len(i_bin)
            str1 = '0' * dec
            nid2_bin += str1 + i_bin
        id2_bin = nid2_bin[:subnet]

        return id1_bin == id2_bin





