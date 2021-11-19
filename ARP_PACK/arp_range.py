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
 

class RangeOfHosts :       
      def __init__(self):
               self.args_command()
               self.Ping_Range()                      
      def Ping_Range(self):     
           try:
               if self.args.network or (self.args.network and self.args.output)  :
                   if "/" not in self.args.network:
                       print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Set the Subnet Netwotk...."+"\n"+R+"="*50+"\n")
                       exit()   
                   if "sudo" not in sys.argv[1]:
                       print(I+D+R+"\n"+"="*50+W+D+I+"\n"+"[*] for arp scan run as root or sudo privileges  "+R+D+"\n"+"="*50+"\n")
                       exit()                     
                   Network     = ipaddress.ip_network('{}'.format(self.args.network), strict=False)
                   Network_ID  = Network.network_address
                   SubNet      = Network.netmask
                   Hosts_range = Network.num_addresses - 2 
                   end_ip = str(Network.broadcast_address).split('.')
                   scop   = "/"
                   try:
                       NetworkID = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.network[-2:]))
                   except Exception:
                          NetworkID = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.network[-1:]))
                   fix  = self.args.network
                   ip,sub = fix.split('/')
                   oct_ip = ip.split('.')
                   start_ip = str(Network_ID).split(".") 
                   if (int(self.args.start)==int(start_ip[3])):
                           print(R+"\n"+"="*50+"\n"+W+I+D+"[+] Erorr       --------------|- Start Ip is Netwotk-ID "+R+"\n"+"="*50+"\n")
                           exit()
                   elif int(self.args.start) < int(self.args.end) and  (int(self.args.end) < int(end_ip[3])):
                           total = int(self.args.end) - int(self.args.start)+1
                   else:
                      if(int(self.args.end) > int(end_ip[3])):
                           print("\n"+"="*50+"\n"+"[+] Erorr       --------------|- range ip out of Subnet-Mask "+"\n"+"="*50+"\n")
                           exit()
                      elif(int(self.args.end))== 255:
                           print("\n"+"="*50+"\n"+"[+] Erorr       --------------|-  end range is  broadcast  "+"\n"+"="*50+"\n")
                           exit()
                   if int(self.args.start) > 256 or int(self.args.end) > 256:
                           print("\n"+"="*50+"\n"+"[+] Erorr       --------------|- Host-Count > 255 Hosts "+"\n"+"="*50+"\n")
                           exit()
                   else:
                       pass  
                   command_argv = str(" ".join(sys.argv))
                   start = timeit.default_timer()
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
                   print("\n[*] HOST INFO-\n"+"="*17+"\n")
                   print("[+] HOST-IP         --------------|- " +  host_ip)
                   print("[+] Mac-Address     --------------|- " +  Mac_Interface)
                   print("[+] Mac-Vendor      --------------|- " + vendor)
                   print("\n[*] NETWORK INFO-\n"+"="*17+"\n")
                   print("[+] Network-ID      --------------|- " +  str(Network_ID))
                   if "/" in self.args.network[-2:]:
                         print("[+] NetWork-Prefix  --------------|- " +  self.args.network[-1:])
                   else:
                        print("[+] NetWork-Prefix  --------------|- " +  self.args.network[-2:])
                   print("[+] Subnet-Mask     --------------|- " +  str(SubNet))
                   print("[+] Frist ip        --------------|- " +  str([ x for x in Network.hosts()][0]))
                   print("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))
                   print("[+] Number of hosts --------------|- " +  str(Hosts_range ))
                   print("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))
                   print("\n[*] Range Host -\n"+"="*17)
                   print("[+] Start-Count     --------------|- " +  self.args.start)
                   print("[+] End-Count       --------------|- " +  self.args.end)
                   print("[+] Host-Count      --------------|- " +  str(total ))
                   print("\n"+"="*50+"\n"+"[*] Host-discover-"+"\n"+"="*20+"\n")
                   if self.args.output:
                         printF  = ""
                         printF  += ("[+] "+ command_argv)+"\n"
                         printF  += ("\n[*] HOST INFO-\n"+"="*17+"\n")+"\n"
                         printF  += ("[+] HOST-IP         --------------|- " +  host_ip)+"\n"
                         printF  += ("[+] Mac-Address     --------------|- " +  Mac_Interface)+"\n"
                         printF  += ("[+] Mac-Vendor      --------------|- " + vendor)+"\n"
                         printF  += ("\n[*] NETWIRK INFO-\n"+"="*17+"\n")+"\n"
                         printF  += ("[+] Network-ID      --------------|- " +  str(Network_ID))+"\n"
                         printF  += ("[+] NetWork-Prefix  --------------|- " +  self.args.network[-2:])+"\n"
                         printF  += ("[+] Subnet-Mask     --------------|- " +  str(SubNet))+"\n"
                         printF  += ("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))+"\n"
                         printF  += ("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))+"\n"
                         printF  += ("[+] Number of hosts --------------|- " +  str(Hosts_range ))+"\n"
                         printF  += ("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))+"\n"                   
                         printF  += ("\n"+"="*50+"\n"+"[*] Host-discover-"+"\n"+"="*20+"\n\n")
                         with open(self.args.output,"w+") as out_put:
                              out_put.write(Banner+"\n"+printF)
                   Hcount = 0
                   dcount = 0
                   for Host_Num in range(int(self.args.start),int(self.args.end)+1) :                      
                        if Host_Num == 256 :  
                              break
                        oct_ip[3] = Host_Num 
                        Host = str(oct_ip).replace("['","").replace("'","").replace(",",".").replace("]","").replace(" ","")               
                        rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW,socket.htons(0x0806))                     
                        rawSocket.settimeout(.20)
                        rawSocket.bind((self.args.Interface,0x0806))
                        source_ip  = bytes(host_ip.encode('utf-8'))
                        dest_ip    = bytes(Host.encode('utf-8'))
                        if dest_ip == source_ip :
                            Hcount  +=1	    
                            print("[+] HOST OnLine     --------------|  " + Host)
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
                                    print("[+] HOST OnLine     --------------|  " + Host)
                                    print("[+] HOST OnLine     --------------|- " + Mac)
                                    print("[+] Mac-Vendor      --------------| " + vendor1)
                                    if self.args.output :
                                       printF += str("[+] HOST OnLine     --------------|  " + Host).strip()+'\n'
                                       printF += str("[*] Mac-Address     ..............|- " + Mac).strip()+'\n'
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
                                print("[+] TRY HOST        --------------| ",Host)
                                time.sleep(0.20)
                                sys.stdout.write('\x1b[1A')
                                sys.stdout.write('\x1b[2K')
                   
                   stop = timeit.default_timer()
                   sec = stop  - start
                   fix_time = time.gmtime(sec)
                   result = time.strftime("%H:%M:%S",fix_time)                
                  
                   print("\n[*] Scan-Result-\n"+"="*14+"\n")
                   print("[+] Total Hosts       --------------|- " + str(Hosts_range))
                   print("[+] Active Hosts      --------------|- " + str(Hcount))
                   print("[+] Inactive Hosts    --------------|- " + str(Hosts_range-Hcount))  
                   print("[+] Run-Time          --------------|- " + result) 
                   print(Banner) 
                   
                   if self.args.output:
                      printF += ("\n[*] SCAN RSULET-\n"+"="*14+"\n")+"\n"
                      printF += ("[+] Total Hosts       --------------|- " + str(Hosts_range))+"\n"
                      printF += ("[+] Active Hosts      --------------|- " + str(Hcount))+"\n"
                      printF += ("[+] Inactive Hosts    --------------|- " + str(Hosts_range- Hcount))+"\n"
                      printF += ("[+] Run-Time          --------------|- " + str(result))+"\n"
                      printF +='\n'
               with open(self.args.output,'w') as out_put :
                    out_put.write(Banner+printF+Banner)   
           except PermissionError :
                   print(I+D+R+"\n"+"="*50+W+D+I+"\n"+"[*]  for arp scan run as root \
                   or sudo privileges   "+R+D+"\n"+"="*50+"\n")           
           except Exception:
                  print("\n"+"="*50+"\n"+"[*] HOST (",self.args.network,")   -------------| ValueError"+"\n"+"="*50+"\n")
           except KeyboardInterrupt:
                  print(Banner)
                  exit()
      def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser.add_argument( '-N',"--network"   ,metavar='' , action=None ) 
              parser.add_argument( '-S',"--start"   ,metavar='' , action=None )
              parser.add_argument( '-O',"--output"   ,metavar='' , action=None)
              parser.add_argument( '-E',"--end"   ,metavar='' , action=None  )
              parser.add_argument( '-I',"--Interface"   ,metavar='' , action=None  )
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   RangeOfHosts()
  
