#!/usr/bin/env python3

import os
import sys
import re
import argparse
import ipaddress
import socket 
import uuid
from subprocess import Popen, PIPE, check_output 
from Package.Banner import *
import subprocess 
import timeit,time
import struct 
import binascii
import random
P= '\033[35m'
W= "\033[1;37m"
R = "\033[0;31m"
D = "\033[1m"
I = "\033[3m"
B = '\033[34m' 
try:
    host_name  = socket.gethostname() 
    host_ip    = str(check_output(['hostname', '--all-ip-addresses'],stderr=subprocess.PIPE)).\
    replace("b'","").replace("'","").replace("\\n","")
    if  host_ip in str(ipaddress.ip_network(self.args.network), strict=False):
          pass
    else:
        if  " " in host_ip : 
            host_ip = host_ip.split()       
            host_ip = host_ip[-1]
except Exception :
    if "/" in sys.argv[2]:
         host_ip = sys.argv[2][:-3]
    else:
         host_ip = sys.argv[2]
   
class Arp_Host_One():
         
        def __init__(self):
           self.args_command()
           self.Ping_command()
                                
        def Ping_command(self):
               try:
                   if self.args.Host or (self.args.Host and self.args.output) :
                      Network     = ipaddress.ip_network('{}'.format(self.args.Host), strict=False)
                      Network_ID  = Network.network_address
                      SubNet      = Network.netmask
                      Hosts_range = Network.num_addresses - 2 
                      command  = "ifconfig " +self.args.Interface
                      Macdb = subprocess.check_output (command,shell=True).decode('utf-8')
                      Macaddr = re.compile(r'(?:[0-9a-fA-F]:?){12}')
                      FMac = str(re.findall(Macaddr ,Macdb)).split()
                      Mac_Interface = str("".join(FMac[0])).replace("'",'').replace(']','').replace("[",'')
                      Mac_Get = Mac_Interface[0:8].replace(":","").upper()
                      Macdb = open('Package/mac-vendor.txt', 'r')
                      Mac = Macdb.readlines()               
                      try:   
                         host_ip_fig = "ifconfig "+ self.args.Interface +" | egrep '([0-9]{1,3}\.){3}[0-9]{1,3}'"    
                         ip_process = str(subprocess.check_output (host_ip_fig,shell=True)).split()
                         host_ip1 = ip_process
                         host_ip = str(host_ip1[2])    
                      except Exception :
                           if "/" in sys.argv[2]:
                               host_ip = sys.argv[2][:-3]
                           else:
                               host_ip = sys.argv[2] 
                      count = 0
                      for line in Mac:
                          line = line.strip()
                          if Mac_Get in line  : 
                             vendor = line[7:].strip() 
                             break 
                          elif Mac_Get not  in line  : 
                             vendor = "Unknown-MAC"
                          count += 1
                      print(D+W+I+"\n[*] HOST INFO-\n"+R+"="*14+"\n")
                      print(I+D+B+"[+] HOST-IP         --------------|- " +  host_ip )
                      print("[+] Mac-Address     --------------|- " +  Mac_Interface)  
                      print("[+] Mac-Vendor      --------------|- " + vendor[0:23])
                      print(D+I+W+"\n[*] NETWORK INFO-\n"+R+"="*14+"\n")
                      print(I+D+B+"[+] Network-ID      --------------|- " +  str(Network_ID))
                      if "/" not in self.args.Host:
                           print("[+] NetWork-Prefix  --------------|- 32")
                      else:
                           if "/" in self.args.Host[-2:]:
                              print("[+] NetWork-Prefix  --------------|- " + str(self.args.Host[-1:]))
                           else:
                              print("[+] NetWork-Prefix  --------------|- " + str(self.args.Host[-2:]))
                      print("[+] Subnet-Mask     --------------|- " +  str(SubNet))
                      print("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))
                      print("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))
                      if "/" not in self.args.Host:
                           print("[+] Number of hosts --------------|- 1")
                      else:
                           print("[+] Number of hosts --------------|- " +  str(Hosts_range ))
                      print("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))
                      print(R+"\n"+"="*50+"\n"+W+"[*] Host-discover-"+R+"\n"+"="*20+"\n")                        
                   if "/"in self.args.Host[-2:]: 
                                          
                        Host = self.args.Host.replace(self.args.Host[-2:],"")
                   elif "/"in self.args.Host[-4:]:
                       
                        Host = self.args.Host.replace(self.args.Host[-3:],"")
                   else:
                        Host = self.args.Host
                   Hcount = 0
                   dcount = 0
                   Host = str(Host)
                   rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW,socket.htons(0x0806))                     
                   rawSocket.settimeout(.50)
                   rawSocket.bind((self.args.Interface,0x0806))
                   source_ip  = bytes(host_ip.encode('utf-8'))
                   dest_ip    = bytes(Host.encode('utf-8'))
                   print(" "+"-"*80) 
                   print("|  "+f"{'   Host    ':<23}","| "+f"{'    Mac-Address    ':<23}"+"| ",f"{'   Mac-Vendor   ':<25}","|")
                   print(" "+"-"*80)        
                   if dest_ip == source_ip :
                        Hcount  +=1	    
                        print(R+"|  "+Y+f"{Host:<23}",R+"|   "+Y+f"{Mac_Interface:<21}"+R+"|  "+Y+f"{vendor[0:23]:<25}",R+"|")  
                        print(Banner)
                        print()
                        exit()
                        interfaceMac = Mac_Interface[0:8].replace(":","").upper()
                   else: 
                        source_mac = binascii.unhexlify(Mac_Interface.replace(":",''))     
                        dest_mac   = b"\xff\xff\xff\xff\xff\xff"
                        protocol   = 0x0806
                        eth_hdr    = struct.pack("!6s6sH",dest_mac,source_mac,protocol)
                        htype      = 1
                        ptype      = 0x0800
                        hlen       = 6
                        plen       = 4 
                        operations = 1
                        src_ip  = socket.inet_aton(str(source_ip).replace("'","").replace('b',""))
                        des_ip  = socket.inet_aton(str(dest_ip).replace("'","").replace('b',""))
                        arp_hdr = struct.pack("!HHBBH6s4s6s4s",htype,ptype,hlen,plen,operations,source_mac,src_ip,dest_mac,des_ip)
                        Packet         = eth_hdr + arp_hdr
                        try:
                            send_packet    = rawSocket.send(Packet) 
                            recv_replay    = rawSocket.recv(1020)
                            rawSocket.close() 
                            Ether_Header   = recv_replay[0:12]
                            unpack_Header  = struct.unpack('!6s6s',Ether_Header)
                            Mac_Source     = str(binascii.hexlify(unpack_Header[1])).replace("b",'',1).replace("'","")
                            Mac = "".join("\\x%s"%Mac_Source [i:i+2] for i in range(0, len(Mac_Source ), 2)).replace("\\x","",1).replace("\\x",':')  
                            unpack1 = str(struct.unpack('!2s',recv_replay[20:22]))   
                            opcodestr = str(unpack1).replace("b'",'').replace("'",'').replace("\\x","").replace(",",'')\
                            .replace("(",'').replace(")",'')    
                            unpack2 = bytes(struct.unpack('!4B',recv_replay[28:32]) )  
                            ip_int = int.from_bytes(unpack2, "big") 
                            ipstr = socket.inet_ntoa(struct.pack('!L', ip_int))                              
                            MacGET= str("".join(Mac[0:8])).replace(":","").upper().strip()
                            Macdb = open('Package/mac-vendor.txt', 'r')
                            MacFile = Macdb.readlines()
                            count = 0                        
                            for line in MacFile:
                                line = line.strip()
                                if MacGET in line : 
                                     vendor1 = line[7:].replace("    ","")                                     
                                     break
                                elif MacGET not  in line:
                                     
                                     vendor1 = " Unknown-MAC" 
                                count += 1   
                                         
                            if "02" in opcodestr and ipstr == Host :
                                    Hcount  +=1	
                                    print(R+"|  "+B+f"{Host:<23}",R+"|   "+P+f"{Mac:<21}"+R+"| "+W+f"{vendor1[0:23]:<25}"+R+"  |"+R)
                                    print()
                                    print(Banner)
                                    exit()
                            else:
                                 pass  
                                       
                        except Exception:
                                dcount +=1
                                Mac = "00:00:00:00:00:00:00"
                                print(R+"|  "+B+f"{Host:<23}",R+"|   "+P+f"{Mac:<21}"+R+"| "+W+f"{'Host is down':<25}"+R+"  |"+R)
                                print()
                                print(Banner)
                                exit()
               except PermissionError :
                   print(I+D+R+"\n"+"="*50+W+D+I+"\n"+"[*]  for arp scan run as root or sudo privileges   "+R+D+"\n"+"="*50+"\n")                   
               except Exception as error :
                   print(R+"\n"+"="*50+W+D+I+"\n"+"[*] Error |",error,R+"\n"+"="*50+"\n")
               except KeyboardInterrupt:
                     print(Banner)
                     if self.args.output :          
                         with open("./Scan-Store/"+self.args.output,'w') as out_put :
                              out_put.write(Banner1+'\n'+printF+Banner1)   
                              id_user =  os.stat("./reachable.py").st_uid 
                              os.chown("./Scan-Store/"+self.args.output, id_user, id_user)
                      
        def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")          
              parser.add_argument( '-O',"--output"   ,metavar='' , action=None )
              parser.add_argument( '-AH',"--Host"   ,metavar='' , action=None  )
              parser.add_argument( '-I',"--Interface" ,metavar='' , action=None,required = True  )
             
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   Arp_Host_One()
        
