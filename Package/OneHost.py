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
 
S='\033[0m' 
W = "\033[1;37m"
R = "\033[0;31m"
D = "\033[1m"
I = "\033[3m"
B = '\033[34m'  
Y='\033[1;33m'

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
     

class Host_One():
          
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
                             vendor = " Unknown-MAC" 
                         count += 1
                      print(W+D+I+"\n[*] HOST INFO-\n"+R+"="*14+"\n")
                      print(B+D+I+"[+] HOST-IP         --------------|- " +  host_ip )
                      print("[+] Mac-Address     --------------|- " +  Mac_Interface)
                      print("[+] Mac-Vendor      --------------|- " + vendor)
                      print(W+I+D+"\n[*] NETWORK INFO-\n"+R+"="*14+"\n")
                      print(B+D+I+"[+] Network-ID      --------------|- " +  str(Network_ID))
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
                      print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Host-discover-"+"\n"+R+"="*20+"\n")
                      
                      if self.args.output:
                           printF  = ""
                           printF  += ("\n[*] HOST INFO-\n"+"="*14+"\n")+"\n"
                           printF  += ("[+] HOST-IP         --------------|- " +  host_ip)+"\n"
                           printF  += ("[+] Mac-Address     --------------|- " +  Mac_Interface)+"\n"
                           printF  += ("[+] Mac-Vendor      --------------|- " + vendor)+"\n"
                           printF  += ("\n[*] NETWIRK INFO-\n"+"="*14+"\n")+"\n"
                           printF  += ("[+] Network-ID      --------------|- " +  str(Network_ID))+"\n"
                           if "/" not in self.args.Host:
                               printF +=("[+] NetWork-Prefix  --------------|- 32")+"\n"
                           else:
                               if "/" in self.args.Host[-2:]:
                                   printF  +=("[+] NetWork-Prefix  --------------|- " + str(self.args.Host[-1:]))+"\n"
                               else:
                                   printF  +=("[+] NetWork-Prefix  --------------|- " + str(self.args.Host[-2:]))+"\n"  
                           printF  += ("[+] Subnet-Mask     --------------|- " +  str(SubNet))+"\n"
                           printF  += ("[+] Start ip        --------------|- " +  str([ x for x in Network.hosts()][0]))+"\n"
                           printF  += ("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))+"\n"
                           printF  += ("[+] Number of hosts --------------|- " +  str(Hosts_range ))+"\n"
                           printF  += ("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))+"\n"
                           printF  += ("\n"+"="*50+"\n"+"[*] Host-discover-"+"\n"+"="*20+"\n\n")
                           with open(self.args.output,"w+") as out_put:
                                out_put.write(Banner+"\n"+printF)
                             
                   if "/"in self.args.Host:
                        Host = self.args.Host.replace(self.args.Host[-3:],"")
                   else:
                        Host = self.args.Host
                   DisCover  = Popen(["ping", "-w1",Host], stdout=PIPE)
                   output    = DisCover.communicate()[0]
                   respons   = DisCover.returncode
                   
                   if respons == 0:
                         if Host == host_ip:
                              print(Y+I+D+"[+] HOST OnLine     --------------| ",host_ip)
                         else:
                              print(B+I+D+"[+] HOST OnLine     --------------| ",Host)
                          
                         if self.args.output :
                             printF = str("[+] HOST OnLine     --------------|  " + Host).strip()
                             with  open (self.args.output,"a") as out_put :
                                  out_put.write(printF+"\n")
                         pid = Popen(["arp", "-a", Host], stdout=PIPE)
                         arp_host = pid.communicate()[0]
                         Mac_arp = str(arp_host)
                         Macaddr = re.compile(r'(?:[0-9a-fA-F]:?){12}')
                         Mac = str(re.findall(Macaddr ,Mac_arp)).replace("['",'').replace("']","")
                         if host_ip == Host :
                               print(Y+D+I+"[*] Mac-Address     ..............|-",Mac_Interface)
                               if self.args.output :
                                  printF = str("[*] Mac-Address     ..............|- "+Mac_Interface).strip()
                                  with open (self.args.output,'a') as out_put :
                                        out_put.write(str(printF+"\n"))
                               interfaceMac = Mac_Interface[0:8].replace(":","").upper()
                                 
                         elif "no match found" in Mac_arp and host_ip != Host :
                               print(B+D+I+"[*] Mac-Address     ..............|- None")
                               if self.args.output :
                                  printF = str("[*] Mac-Address     ..............|- None")
                                  with open (self.args.output,'a') as out_put :
                                        out_put.write(str(printF+"\n"))
                                  interfaceMac = Mac_Interface[0:8].replace(":","").upper()
                                 
                         else:
                               print(W+D+I+"[*] Mac-Address     ..............|-",Mac)
                               if self.args.output :  
                                  printF = str("[*] Mac-Address     ..............|- "+Mac).strip()
                                  with open (self.args.output,'a') as out_put :
                                        out_put.write(str(printF+"\n"))
                             #  interfaceMac = Mac_Interface[0:8].replace(":","").upper()     
                         MacGET= Mac[0:8].replace(":","").upper()

                         Macdb = open('Package/mac-vendor.txt', 'r')
                         MacFile = Macdb.readlines()
                         
                         count = 0
                         for line in MacFile  :
                            
                             line = line.strip()
                             if  MacGET in line  : 
                                 vendor1 = line[7:].strip()
                                 break
                             elif  MacGET not  in line  : 
                                 vendor1 = " Unknown-MAC" 
                             count += 1                              
  
                         if host_ip == Host :
                               print(Y+D+I+"[+] Mac-Vendor      --------------|  " +vendor)
                               if self.args.output :
                                  printF = str("[+] Mac-Vendor      --------------|  " +vendor).strip()
                                  with open(self.args.output ,"a") as out_put :
                                       out_put.write(str(printF+"\n"))
                                      
                         elif "None" in Mac and host_ip != Host :
                               print(B+D+I+"[+] Mac-Vendor      --------------|  None ")
                               if self.args.output :
                                  printF = str("[+] Mac-Vendor      --------------|  None")
                                  with open(self.args.output ,"a") as out_put :
                                       out_put.write(str(printF+"\n"))
                         else:
                               print(I+D+B+"[+] Mac-Vendor      --------------|  " +vendor1)
                               if self.args.output :    
                                  printF = str("[+] Mac-Vendor      --------------| " +vendor1).strip()
                                  with open(self.args.output ,"a") as out_put :
                                        out_put.write(str(printF+"\n"))           
                         print()
                         if self.args.output:
                               with open(self.args.output,"a") as out_put :
                                    out_put.write("\n")
                   else:
                         print(I+R+D+"[*] HOST  (",Host,")   -------------| Not response !!")      
                   print(Banner) 
                   if self.args.output:
                         with open(self.args.output,'a') as out_put :
                              out_put.write(Banner) 
               except Exception  :                       
                      print(R+"\n"+"="*50+"\n"+D+I+W+"[*] HOST (",self.args.Host,")   -------------| ValueError"+R+"\n"+"="*50+"\n")
               except KeyboardInterrupt:
                      print(Banner)
                      if self.args.output:
                           with open(self.args.output,'a') as out_put :
                                 out_put.write(Banner)
                   
        def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")          
              parser.add_argument( '-O',"--output"   ,metavar='' , action=None )
              parser.add_argument( '-H',"--Host"   ,metavar='' , action=None  )
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   Host_One()
