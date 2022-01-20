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
S ='\033[0m' 
W = "\033[1;37m"
R = "\033[0;31m"
D = "\033[1m"
I = ""
B = '\033[34m'  
Y='\033[1;33m' 

class Arp_Network():
         
    def __init__(self):
          self.args_command()
          self.Ping_command()  
    def Change_mac(self):
           if self.args.Mac and 'true' in sys.argv:
              try:
                  Mac_list =  ['FC:0F:E6:','00:12:EE:','00:1E:DC:','78:84:3C:',
                               '00:26:B9:','14:FE:B5:','BC:30:5B:','D0:67:E5:',
                               '10:1D:C0:','78:25:AD:','A0:0B:BA:','E8:11:32:',
                               'F8:1E:DF:','E0:F8:47:','A4:B1:97:','7C:6D:62:',
                              ] 
                  Mac_list= random.choice(Mac_list)                  
                  Mac_Cook  ="".join( f'{random.randrange(16**8):x}')
                  Mac_Host = ':'.join(Mac_Cook[i:i+2] for i in range(0,6,2)).upper()
                  self.Mac_addr =  Mac_list + Mac_Host  
                  command  = "ifconfig  "+self.args.Interface + " | grep ether"
                  Current_Mac_P = subprocess.check_output (command,shell=True).decode('utf-8')
                  Current_Mac_C = re.compile(r'(?:[0-9a-fA-F]:?){12}')
                  Current_Mac_F = re.findall(Current_Mac_C , Current_Mac_P)
                  self.Current_Mac_G = str("".join(Current_Mac_F[0]))
                  ifconfig_down = "sudo ifconfig "+self.args.Interface+" down"
                  ifconfig_mac_change = "sudo ifconfig "+self.args.Interface+ " hw ether "+self.Mac_addr
                  ifconfig_up = "sudo ifconfig "+self.args.Interface+" up"
                  os.system(ifconfig_down)
                  config  = os.system(ifconfig_mac_change)
                  os.system(ifconfig_up)   
                  print(W+D+I+"\n[*] Mac-chanage-\n"+R+"="*14+"\n")
                  print(D+I+B+"[+] New Mac          --------------|- " + self.Mac_addr )  
              except Exception :
                       print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Error   -------------| Set InterFace argmint"+R+"\n"+"="*50+"\n")
                       exit()
           else:
                print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Error   -------------| Set -M/--Mac true"+R+"\n"+"="*50+"\n")
                exit()                                                                                                 
    def Ping_command(self):   
           try:
               start = timeit.default_timer()
               Network     = ipaddress.ip_network('{}'.format(self.args.arpnetwork), strict=False)
               Network_ID  = Network.network_address
               SubNet      = Network.netmask
               Hosts_range = Network.num_addresses - 2 
               scop   = "/"
               if self.args.Mac:  
                      try:
                          linker  = "ip link show "+self.args.Interface
                          link_Mac= subprocess.check_output (linker,shell=True).decode('utf-8')  
                          real_Mac_split = link_Mac.split() 
                          if "permaddr" in  real_Mac_split:
                              self.Mac_Interface1 = real_Mac_split[-1] 
                          else: 
                             self.Mac_Interface1 = real_Mac_split[-3]
                      except Exception :
                         print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Error   -------------| Set InterFace argmint"+R+"\n"+"="*50+"\n")
                         exit()                
               try:
                  Network  = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.arpnetwork[-2:]))
               except Exception :
                  Network  = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.arpnetwork[-1:]))
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
               if self.args.arpnetwork and self.args.Interface :
                   if "/" not in self.args.arpnetwork:
                       print(I+D+R+"\n"+"="*50+W+D+I+"\n"+"[*] Set the Subnet Netwotk...."+R+D+"\n"+"="*50+"\n")
                       exit()           
                   print(W+D+I+"\n[*] HOST INFO-\n"+R+"="*14+"\n")
                   print(D+I+B+"[+] HOST-IP         --------------|- " +  host_ip)
                   if self.args.Mac :
                      print("[+] Mac-Address     --------------|- " +  self.Mac_Interface1)
                   else:  
                       print("[+] Mac-Address     --------------|- " +  Mac_Interface)  
                   print("[+] Mac-Vendor      --------------|- " + vendor)
                   if self.args.Mac:
                      self.Change_mac()
                   print("[+] Mac-Vendor      --------------|- " + vendor)
                   print(W+I+D+"\n[*] NETWORK INFO-\n"+R+"="*14+"\n")
                   print(B+I+D+"[+] Network-ID      --------------|- " +  str(Network_ID))
                   if "/" in self.args.arpnetwork[-2:] :
                      print("[+] NetWork-Prefix  --------------|- " +  self.args.arpnetwork[-1:])
                   else:
                      print("[+] NetWork-Prefix  --------------|- " +  self.args.arpnetwork[-2:])
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
                         if "/" in self.args.arpnetwork[-2:]:
                             printF  += ("[+] NetWork-Prefix  --------------|- " +  self.args.arpnetwork[-1:])+"\n"
                         else:
                             printF  += ("[+] NetWork-Prefix  --------------|- " +  self.args.arpnetwork[-2:])+"\n"
                         printF  += ("[+] Subnet-Mask     --------------|- " +  str(SubNet))+"\n"
                         printF  += ("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))+"\n"
                         printF  += ("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))+"\n"
                         printF  += ("[+] Number of hosts --------------|- " +  str(Hosts_range ))+"\n"
                         printF  += ("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))+"\n"
                         printF  += ("\n"+"="*50+"\n"+"[*] Host-discover-"+"\n"+"="*20+"\n\n")    
                         printF += str(" "+"-"*80)+"\n" 
                         printF += str("|  "+f"{'   Host    ':<23}"+"| "+f"{'    Mac-Address    ':<23}"+"| "+f"{'   Mac-Vendor   ':<28}"+"|")+'\n'
                         printF += str(" "+"-"*80)+'\n'             
                   scop   = "/"
                   Network  = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.arpnetwork[-2:]))
                   Hcount = 0
                   dcount = 0
                   print(" "+"-"*80) 
                   print("|  "+f"{'   Host    ':<23}","| "+f"{'    Mac-Address    ':<23}"+"| ",f"{'   Mac-Vondor   ':<25}","|")
                   print(" "+"-"*80)
                   
                   for Host in Network .hosts():
                         
                        Host = str(Host)
                        rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW,socket.htons(0x0806))                     
                        rawSocket.settimeout(1)
                        rawSocket.bind((self.args.Interface,0x0806))
                        source_ip  = bytes(host_ip.encode('utf-8'))
                        dest_ip    = bytes(Host.encode('utf-8'))
                        if dest_ip == source_ip :
                            Hcount  +=1	   
                            print(R+"|  "+Y+f"{Host:<23}",R+"|   "+Y+f"{Mac_Interface:<21}"+R+"|  "+Y+f"{vendor[0:23]:<25}",R+"|")  
                            if self.args.output : 
                                printF +="|  "+f"{Host:<23}"+"|   "+f"{Mac_Interface:<21}"+"|  "+f"{vendor[0:23]:<27}"+"|"+'\n'  
                            interfaceMac = Mac_Interface[0:8].replace(":","").upper()
                        else:
                            if self.args.Mac:      
                                   source_mac = binascii.unhexlify(self.Mac_addr.replace(":",''))
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
                                             
                                if "02" in opcodestr and ipstr == Host :
                                    Hcount  +=1	
                                    print(R+"|  "+B+f"{Host:<23}",R+"|   "+P+f"{Mac:<21}"+R+"| "+W+f"{vendor1[0:23]:<25}"+R+"  |"+R)
                                    if self.args.output :
                                       printF +=str("|  "+f"{Host:<23}"+"|   "+f"{Mac:<21}"+"| "+f"{vendor1[0:23]:<26}"+"  |")+'\n' 
                                else:
                                     if "01" in opcodestr :
                                          pass
                                        # sys.stdout.write('\x1b[1A')
                                         #sys.stdout.write('\x1b[2K')                             
                          
                            except socket.timeout :
                                dcount +=1 
                                host_split = Host.split(".")                              
                                print(R+"|  "+Y+f"{Host:<23}",R+"|"+P+f"{'   00:00:00:00:00:00   ':<21}"+R+" | "+B+f"{'   ----------------   ':<26}",R+"|")
                                sys.stdout.write('\x1b[1A')
                                sys.stdout.write('\x1b[2K')
                   
                   stop = timeit.default_timer()
                   sec = stop  - start
                   fix_time = time.gmtime(sec)
                   result = time.strftime("%H:%M:%S",fix_time)                
                   if self.args.Mac:              
                      ifconfig_down = "sudo ifconfig "+self.args.Interface+" down"
                      ifconfig_mac_change = "sudo ifconfig "+self.args.Interface+ " hw ether "+self.Mac_Interface1
                      ifconfig_up = "sudo ifconfig "+self.args.Interface+" up"
                      os.system(ifconfig_down)
                      config  = os.system(ifconfig_mac_change)
                      os.system(ifconfig_up)   
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
                      with open("./Scan-Store/"+self.args.output,'w') as out_put :
                         out_put.write(Banner1+'\n\n'+printF+Banner1)
                         id_user =  os.stat("./reachable.py").st_uid 
                         os.chown("./Scan-Store/"+self.args.output, id_user, id_user)
                         exit()
                   else: 
                       exit()   
           except PermissionError :
                   print(I+D+R+"\n"+"="*50+W+D+I+"\n"+"[*]  for arp scan run as root or sudo privileges   "+R+D+"\n"+"="*50+"\n")       
           except Exception:
                print(R+"\n"+"="*50+W+D+I+"\n"+"[*] ValueError (",self.args.arpnetwork,")-------------| wrong format IP "+R+"\n"+"="*50+"\n")
           except KeyboardInterrupt:
                  print(Banner)
                  if self.args.output :          
                       with open("./Scan-Store/"+self.args.output,'w') as out_put :
                            out_put.write(Banner1+'\n'+printF+Banner1)   
                            id_user =  os.stat("./reachable.py").st_uid 
                            os.chown("./Scan-Store/"+self.args.output, id_user, id_user)
                
    def args_command(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
            parser.add_argument( '-AN',"--arpnetwork"   ,metavar='' , action=None  )
            parser.add_argument( '-O',"--output"    ,metavar='' , action=None  )
            parser.add_argument( '-I',"--Interface" ,metavar='' , action=None  )
            parser.add_argument( '-M',"--Mac" ,metavar='' , action=None  )
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
                 pass
            else:
                 parser.print_help()
                 exit()                                        
       
if __name__=="__main__":
   Arp_Network()
