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

S ='\033[0m' 
W = "\033[1;37m"
R = "\033[0;31m"
D = "\033[1m"
I = "\033[3m"
B = '\033[34m'  
Y='\033[1;33m' 

class Arp_Network():
          
    def __init__(self):
          self.args_command()
          self.Ping_command()                  
    def Ping_command(self):   
           try:
               start = timeit.default_timer()
               Network     = ipaddress.ip_network('{}'.format(self.args.network), strict=False)
               Network_ID  = Network.network_address
               SubNet      = Network.netmask
               Hosts_range = Network.num_addresses - 2 
               scop   = "/"
               try:
                  Network  = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.network[-2:]))
               except Exception :
                  Network  = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.network[-1:]))
               command_argv = str(" ".join(sys.argv))       
               Mac_Interface = ':'.join(re.findall('..', '%012x' % uuid.getnode())) 
               Mac_Get = Mac_Interface[0:8].replace(":","").upper()
               Macdb = open('Package/mac-vendor.txt', 'r')
               Mac = Macdb.readlines()               
               try:
                  host_name  = socket.gethostname() 
                  host_ip    = str(check_output(['hostname', '--all-ip-addresses'],stderr=subprocess.PIPE)).\
                  replace("b'","").replace("'","").replace("\\n","")
                  Network1 = str(Network )
                  if  " " in host_ip : 
                     host_ip = host_ip.split()
                     host_ip_0 = str(host_ip[0])
                     if ipaddress.ip_address(host_ip_0) in ipaddress.ip_network(Network1):              
                         host_ip = host_ip_0
                         command  = "ifconfig | grep 'ether'"
                         Macdb = subprocess.check_output (command,shell=True).decode('utf-8')
                         Macaddr = re.compile(r'(?:[0-9a-fA-F]:?){12}')
                         FMac = re.findall(Macaddr ,Macdb)
                         Mac_Interface = str("".join(FMac[0]))
                         Mac_Get = Mac_Interface[0:8].replace(":","").upper()
                     else:                         
                         host_ip = str(host_ip[-1])
                         command  = "ifconfig | grep 'ether'"
                         Macdb = subprocess.check_output (command,shell=True).decode('utf-8')
                         Macaddr = re.compile(r'(?:[0-9a-fA-F]:?){12}')
                         FMac = re.findall(Macaddr ,Macdb)
                         Mac_Interface = str("".join(FMac[-1]))
                         Mac_Get = Mac_Interface[0:8].replace(":","").upper()
               except Exception :
                      if "/" in sys.argv[2]:
                         host_ip = sys.argv[2][:-3]
                      else:
                         host_ip = sys.argv[2] 
               count = 0
               for line in Mac :
                    line = line.strip()
                    if Mac_Get in line  : 
                          vendor = line[7:].strip() 
                          break 
                    elif Mac_Get not  in line  : 
                         vendor = "Unknown-MAC" 
               count += 1
               if self.args.network and self.args.Interface :
                   if "/" not in self.args.network:
                       print(I+D+R+"\n"+"="*50+W+D+I+"\n"+"[*] Set the Subnet Netwotk...."+R+D+"\n"+"="*50+"\n")
                       exit()           
                   print(W+D+I+"\n[*] HOST INFO-\n"+R+"="*14+"\n")
                   print(D+I+B+"[+] HOST-IP         --------------|- " +  host_ip)
                   print("[+] Mac-Address     --------------|- " +  Mac_Interface)
                   print("[+] Mac-Vendor      --------------|- " + vendor)
                   print(W+I+D+"\n[*] NETWORK INFO-\n"+R+"="*14+"\n")
                   print(B+I+D+"[+] Network-ID      --------------|- " +  str(Network_ID))
                   if "/" in self.args.network[-2:] :
                      print("[+] NetWork-Prefix  --------------|- " +  self.args.network[-1:])
                   else:
                      print("[+] NetWork-Prefix  --------------|- " +  self.args.network[-2:])
                   print("[+] Subnet-Mask     --------------|- " +  str(SubNet))
                   print("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))
                   print("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))
                   print("[+] Number of hosts --------------|- " +  str(Hosts_range ))
                   print("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))
                   print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Host-discover-"+R+"\n"+"="*20+"\n")
                   if self.args.output:
                         printF  = ""
                         printF  += ("[+] "+ command_argv)+"\n"
                         printF  += ("\n[*] HOST INFO-\n"+"="*14+"\n")+"\n"
                         printF  += ("[+] HOST-IP         --------------|- " +  host_ip)+"\n"
                         printF  += ("[+] Mac-Address     --------------|- " +  Mac_Interface)+"\n"
                         printF  += ("[+] Mac-Vendor      --------------|- " + vendor)+"\n"
                         printF  += ("\n[*] NETWIRK INFO-\n"+"="*14+"\n")+"\n"
                         printF  += ("[+] Network-ID      --------------|- " +  str(Network_ID))+"\n"
                         if "/" in self.args.network[-2:]:
                             printF  += ("[+] NetWork-Prefix  --------------|- " +  self.args.network[-1:])+"\n"
                         else:
                             printF  += ("[+] NetWork-Prefix  --------------|- " +  self.args.network[-2:])+"\n"
                         printF  += ("[+] Subnet-Mask     --------------|- " +  str(SubNet))+"\n"
                         printF  += ("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))+"\n"
                         printF  += ("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))+"\n"
                         printF  += ("[+] Number of hosts --------------|- " +  str(Hosts_range ))+"\n"
                         printF  += ("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))+"\n"
                         printF  += ("\n"+"="*50+"\n"+"[*] Host-discover-"+"\n"+"="*20+"\n\n")                 
                   scop   = "/"
                   Network  = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.network[-2:]))
                   Hcount = 0
                   dcount = 0
                   for Host in Network .hosts():
                        Host = str(Host)
                        rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW,socket.htons(0x0806))                     
                        rawSocket.settimeout(.20)
                        rawSocket.bind((self.args.Interface,0x0806))
                        source_ip  = bytes(host_ip.encode('utf-8'))
                        dest_ip    = bytes(Host.encode('utf-8'))
                        if dest_ip == source_ip :
                            Hcount  +=1	    
                            print(Y+D+I+"[+] HOST OnLine     --------------|  " + Host)
                            print("[*] Mac-Address     ..............|- " + Mac_Interface)
                            print("[+] Mac-Vendor      --------------|  " + vendor+'\n')
                            if self.args.output :
                                printF += str("[+] HOST OnLine     --------------|  " + Host).strip()+'\n'
                                printF += str("[*] Mac-Address     ..............|- " + Mac_Interface).strip()+'\n'
                                printF += str("[+] Mac-Vendor      --------------|  " + vendor).strip()+'\n'
                                printF +='\n'
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
                                MacGET= str("".join(Mac[0:8])).replace(":","").upper()
                                Macdb = open('Package/mac-vendor.txt', 'r')
                                MacFile = Macdb.readlines()
                                count = 0                        
                                for line in MacFile:
                                    line = line.strip()
                                    if MacGET in line  : 
                                        vendor1 = line[7:] 
                                        break
                                    elif MacGET not  in line:
                                        vendor1 = " Unknown-MAC" 
                                    count += 1           
                                if "02" in opcodestr :
                                    Hcount  +=1	
                                    print(B+D+I+"[+] HOST OnLine     --------------|  " + Host)
                                    print(W+D+I+"[*] Mac-Address     ..............|- " + Mac[0:17])
                                    print(D+B+I+"[+] Mac-Vendor      --------------| " + vendor1)
                                    if self.args.output :
                                       printF += str("[+] HOST OnLine     --------------|  " + Host).strip()+'\n'
                                       printF += str("[*] Mac-Address     ..............|- " + Mac[0]).strip()+'\n'
                                       printF += str("[+] Mac-Vendor      --------------| " + vendor1).strip()+'\n'
                                       printF +='\n'
                                else:
                                     if "01" in opcodestr :
                                          print(D+I+Y+"[+] TRY HOST        --------------| ",Host,end='')
                                          sys.stdout.write('\x1b[1A')
                                          sys.stdout.write('\x1b[2K')
                                          pass
                                print()                             
                            except Exception:
                                dcount +=1
                                print(D+I+Y+"[+] TRY HOST        --------------| ",Host)
                                time.sleep(.20)
                                sys.stdout.write('\x1b[1A')
                                sys.stdout.write('\x1b[2K')

                   stop = timeit.default_timer()
                   sec = stop  - start
                   fix_time = time.gmtime(sec)
                   result = time.strftime("%H:%M:%S",fix_time)                
                  
                   print(W+D+I+"\n[*] Scan-Result-\n"+R+"="*14+"\n")
                   print(B+D+I+"[+] Total Hosts       --------------|- " + Y,str(Hosts_range)),S
                   print(B+D+I+"[+] Active Hosts      --------------|- " + Y,str(Hcount)),S
                   print(B+D+I+"[+] Inactive Hosts    --------------|- " + Y, str(Hosts_range-Hcount)),S  
                   print(B+D+I+"[+] Run-Time          --------------|- " + Y,str(result)),S
                   print(Banner)        
                   if self.args.output:
                      printF += ("\n[*] SCAN RSULET-\n"+"="*14+"\n")+"\n"
                      printF += ("[+] Total Hosts       --------------|- " + str(Hosts_range))+"\n"
                      printF += ("[+] Active Hosts      --------------|- " + str(Hcount))+"\n"
                      printF += ("[+] Inactive Hosts    --------------|- " + str(Hosts_range- Hcount))+"\n"
                      printF += ("[+] Run-Time          --------------|- " + str(result))+"\n"
                      printF +='\n'
                      with open(self.args.output,'w') as out_put :
                         out_put.write(Banner+'\n\n'+printF+Banner)
                         exit()
                   else: 
                       exit()   
           except PermissionError :
                   print(I+D+R+"\n"+"="*50+W+D+I+"\n"+"[*]  for arp scan run as root or sudo privileges   "+R+D+"\n"+"="*50+"\n")       
           except Exception:
                print(R+"\n"+"="*50+W+D+I+"\n"+"[*] ValueError (",self.args.network,")-------------| wrong format IP "+R+"\n"+"="*50+"\n")
           except KeyboardInterrupt:
               print(Banner)
               if self.args.output:
                  with open(self.args.output,'a') as out_put :
                     out_put.write(Banner)
                
    def args_command(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
            parser.add_argument( '-N',"--network"   ,metavar='' , action=None  )
            parser.add_argument( '-O',"--output"    ,metavar='' , action=None  )
            parser.add_argument( '-I',"--Interface" ,metavar='' , action=None  )
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
                 pass
            else:
                 parser.print_help()
                 exit()                                        
       
if __name__=="__main__":
   Arp_Network()
