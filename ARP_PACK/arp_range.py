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
 

class Range_arp_host :       
      def __init__(self):
               self.args_command()
               self.arp_Range()  
      def Change_mac(self):
           if self.args.Mac and 'true' in sys.argv :
              try:
                  if os.geteuid() == 0 :
                     pass
                  else:
                      print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Error   -------------|  root or sudo privileges"+R+"\n"+"="*50+"\n")
                      exit()                     
                  mac_list =  ['FC:0F:E6:','00:12:EE:','00:1E:DC:','78:84:3C:',
                               '00:26:B9:','14:FE:B5:','BC:30:5B:','D0:67:E5:',
                               '10:1D:C0:','78:25:AD:','A0:0B:BA:','E8:11:32:',
                               'F8:1E:DF:','E0:F8:47:','A4:B1:97:','7C:6D:62:',
                               '00:0A:F3:','00:0C:86:','B4:A4:E3:','FC:FB:FB:',
                              ] 
                              
                  Mac_list= random.choice(mac_list)                  
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
                  timer = 20
                  vendor_chanage = ''
                  if   Mac_list in str("".join(mac_list[0:4]))   :
                       vendor_chanage = 'Sony'
                  elif Mac_list in   str("".join(mac_list[4:8])) :
                       vendor_chanage = 'Dell'
                  elif Mac_list in str("".join(mac_list[8:12]))  :
                       vendor_chanage = 'Samsung'
                  elif Mac_list in str("".join(mac_list[12:16])) :
                       vendor_chanage = 'Apple'     
                  elif Mac_list in str("".join(mac_list[16:20])) :
                       vendor_chanage = 'Cisco'                     
                  for timered  in range (timer) :
                      time.sleep(1)
                      timer -=1
                      print(D+I+B+"\r[+] [ "+P+self.args.Interface+B+ " ]  in preparation   " + Y +('#'*timered+S ) )
                      sys.stdout.write('\x1b[1A')
                      sys.stdout.write('\x1b[2K')
                  print(D+I+B+"[+] New Mac          --------------|- " + self.Mac_addr +Y+" [ "+vendor_chanage+" ] ")  
                  time.sleep(1)
              except Exception :             
                       print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Error   -------------| Set InterFace argument"+R+"\n"+"="*50+"\n")
                       exit()
           else:
                print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Error   -------------| Set -M/--Mac true"+R+"\n"+"="*50+"\n")
                exit()                                                                                                   
      def arp_Range(self):     
           try:
               if self.args.arpnetwork or (self.args.arpnetwork and self.args.output)  :
                   if "/" not in self.args.arpnetwork:
                       print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Set the Subnet Netwotk...."+"\n"+R+"="*50+"\n")
                       exit()   
                   Network     = ipaddress.ip_network('{}'.format(self.args.arpnetwork), strict=False)
                   Network_ID  = Network.network_address
                   SubNet      = Network.netmask
                   Hosts_range = Network.num_addresses - 2 
                   end_ip = str(Network.broadcast_address).split('.')
                   fix  = self.args.arpnetwork
                   ip,sub = fix.split('/')
                   oct_ip = ip.split('.')
                   start_ip = str(Network_ID).split(".")                   
                   command_argv = str(" ".join(sys.argv))
                   start = timeit.default_timer()
                   if int(self.args.start)  not in range(int(start_ip[3]),int(end_ip[3])) \
                   or int(self.args.end)  not in range(int(start_ip[3]),int(end_ip[3])) :
                          print('[+] Start subnet  : ',start_ip[3])
                          print('[+] end  subnet   : ',end_ip[3])
                          print(D+R+I+"[+] Range Error     --------------| Hosts Count out of range Network Subnet" )
                          exit()
                   elif int(self.args.start) >= int (self.args.end) : 
                          print('[+] Start Host  : ',start_ip[3])
                          print('[+] end   Host   : ',end_ip[3])
                          print("[+] Range Error     --------------|  Wrong arithmetic Operation " )
                          exit()    
                   elif int(self.args.start) < int(self.args.end) :
                        total = int(self.args.end) - int(self.args.start)        
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
                         print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Error   -------------| Set InterFace argument"+R+"\n"+"="*50+"\n")
                         exit()                
                   try:
                       NetworkID = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.arpnetwork[-2:]))
                   except Exception:
                          NetworkID = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.arpnetwork[-1:]))
                 
                   command  = "ifconfig " +self.args.Interface
                   Macdb = subprocess.check_output (command,shell=True).decode('utf-8')
                   Macaddr = re.compile(r'(?:[0-9a-fA-F]:?){12}')
                   FMac = str(re.findall(Macaddr ,Macdb)).split()
                   try:
                      Mac_Interface = str("".join(FMac[-1])).replace("'",'').replace(']','').replace("[",'')
                   except Exception :
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
                   for line in Mac :
                       line = line.strip()
                       if Mac_Get in line  : 
                            vendor = line[7:].strip() 
                            break 
                       elif Mac_Get not  in line  : 
                             vendor = "Unknown-MAC" 
                       count += 1
                   print(W+D+I+"\n[*] HOST INFO-\n"+R+"="*17+"\n")
                   print(D+I+B+"[+] HOST-IP         --------------|- " +  host_ip)
                   if self.args.Mac :
                      print("[+] Mac-Address     --------------|- " +  self.Mac_Interface1)
                   else:  
                       print("[+] Mac-Address     --------------|- " +  Mac_Interface)  
                      
                   print("[+] Mac-Vendor      --------------|- " + vendor[0:23])
                   if self.args.Mac:
                      print(W+D+I+"\n[*] Mac-chanage-\n"+R+"="*14+"\n")
                      self.Change_mac()
                   print(W+I+D+"\n[*] NETWORK INFO-\n"+R+"="*17+"\n")
                   print(B+I+D+"[+] Network-ID      --------------|- " +  str(Network_ID))
                   if "/" in self.args.arpnetwork[-2:]:
                         print("[+] NetWork-Prefix  --------------|- " +  self.args.arpnetwork[-1:])
                   else:
                        print("[+] NetWork-Prefix  --------------|- " +  self.args.arpnetwork[-2:])
                   print(B+I+D+"[+] Subnet-Mask     --------------|- " +  str(SubNet))
                   print("[+] Frist ip        --------------|- " +  str([ x for x in Network.hosts()][0]))
                   print("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))
                   print("[+] Number of hosts --------------|- " +  str(Hosts_range ))
                   print("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))
                   print(W+I+D+"\n[*] Range Host -\n"+R+"="*17)
                   print(B+I+D+"[+] Start-Count     --------------|- " + Y, self.args.start)
                   print(B+D+I+"[+] End-Count       --------------|- " + Y, self.args.end)
                   print(B+D+I+"[+] Host-Count      --------------|- " + Y, str(total ))
                   print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Host-discover-"+"\n"+R+"="*20+"\n")
                   if self.args.output:
                         printF  = ""
                         printF  += ("[+] "+ command_argv)+"\n"
                         printF  += ("\n[*] HOST INFO-\n"+"="*17+"\n")+"\n"
                         printF  += ("[+] HOST-IP         --------------|- " +  host_ip)+"\n"
                         if self.args.Mac :
                               printF  += ("[+] Mac-Address     --------------|- " +  self.Mac_Interface1)+"\n"
                         else:
                               printF  += ("[+] Mac-Address     --------------|- " +  Mac_Interface)+"\n" 
                         printF  += ("[+] Mac-Vendor      --------------|- " + vendor[0:23])+"\n"
                         printF  += ("\n[*] NETWIRK INFO-\n"+"="*17+"\n")+"\n"
                         printF  += ("[+] Network-ID      --------------|- " +  str(Network_ID))+"\n"
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
                   Hcount = 0
                   dcount = 0
                   print(" "+"-"*80) 
                   print("|  "+f"{'   Host    ':<23}","| "+f"{'    Mac-Address    ':<23}"+"| ",f"{'   Mac-Vondor   ':<25}","|")
                   print(" "+"-"*80)
                   
                   for Host_Num in range(int(self.args.start),int(self.args.end)+1) :                      
                        if Host_Num == 256 :  
                              break
                    #    command = "ip -s -s neigh flush all  > output "
                    #    subprocess.call(command,shell=True,stderr=subprocess.PIPE) 
                    #    os.remove("output")
                        oct_ip[3] = Host_Num 
                        Host = str(oct_ip).replace("['","").replace("'","").replace(",",".").replace("]","").replace(" ","")               
                        rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW,socket.htons(0x0806))                     
                        rawSocket.settimeout(0.50)
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
                                #rawSocket.close() 
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
                            except Exception:
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
                   print(B+D+I+"[+] Total Hosts       --------------|- " + Y,str(total)),S
                   print(B+D+I+"[+] Active Hosts      --------------|- " + Y,str(Hcount)),S
                   print(B+D+I+"[+] Inactive Hosts    --------------|- " + Y, str(total-Hcount)),S  
                   print(B+D+I+"[+] Run-Time          --------------|- " + Y,str(result)),S
                   print(Banner)        
                   
                   if self.args.output:
                      printF += ("\n[*] SCAN RSULET-\n"+"="*14+"\n")+"\n"
                      printF += ("[+] Total Hosts       --------------|- " + str(total))+"\n"
                      printF += ("[+] Active Hosts      --------------|- " + str(Hcount))+"\n"
                      printF += ("[+] Inactive Hosts    --------------|- " + str(total- Hcount))+"\n"
                      printF += ("[+] Run-Time          --------------|- " + str(result))+"\n"
                      printF +='\n'
               if self.args.output :          
                    with open("./Scan-Store/"+self.args.output,'w') as out_put :
                        out_put.write(Banner1+'\n'+printF+Banner1)   
                        id_user =  os.stat("./reachable.py").st_uid 
                        os.chown("./Scan-Store/"+self.args.output, id_user, id_user)
           except PermissionError :
                   print(I+D+R+"\n"+"="*50+W+D+I+"\n"+"[*] for arp scan run as root or sudo privileges   "+R+D+"\n"+"="*50+"\n")           
           except Exception as error :
                   print(R+"\n"+"="*50+W+D+I+"\n"+"[*] Error |",error,R+"\n"+"="*50+"\n")
           except KeyboardInterrupt:
                  print(Banner)
                  if self.args.output :          
                        with open("./Scan-Store/"+self.args.output,'w') as out_put :
                             out_put.write(Banner1+'\n'+printF+Banner1)   
                             id_user =  os.stat("./reachable.py").st_uid 
                             os.chown("./Scan-Store/"+self.args.output, id_user, id_user)
                  if self.args.Mac:              
                        ifconfig_down = "sudo ifconfig "+self.args.Interface+" down"
                        ifconfig_mac_change = "sudo ifconfig "+self.args.Interface+ " hw ether "+self.Mac_Interface1
                        ifconfig_up = "sudo ifconfig "+self.args.Interface+" up"
                        os.system(ifconfig_down)
                        config  = os.system(ifconfig_mac_change)
                        os.system(ifconfig_up)
                  
      def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser.add_argument( '-AN',"--arpnetwork"    ) 
              parser.add_argument( '-S',"--start"      )
              parser.add_argument( '-O',"--output"     )
              parser.add_argument( '-E',"--end"        )
              parser.add_argument( '-I',"--Interface" ,metavar='' , action=None,required = True  )
              parser.add_argument( '-M',"--Mac"  )
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   Range_arp_host()
  
  
  
  
  
