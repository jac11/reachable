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
P= '\033[35m'
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
                           printF += str(" "+"-"*80)+"\n" 
                           printF += str("|  "+f"{'   Host    ':<23}"+"| "+f"{'    Mac-Address    ':<23}"+"| "+f"{'   Mac-Vondor   ':<28}"+"|")+'\n'
                           printF += str(" "+"-"*80)+'\n'             
                           with open(self.args.output,"w+") as out_put:
                                out_put.write(Banner+"\n"+printF)
                   print(" "+"-"*80) 
                   print("|  "+f"{'   Host    ':<23}","| "+f"{'    Mac-Address    ':<23}"+"| ",f"{'   Mac-Vondor   ':<25}","|")
                   print(" "+"-"*80)                         
                   if "/"in self.args.Host:
                        Host = self.args.Host.replace(self.args.Host[-3:],"")
                   else:
                        Host = self.args.Host
                   Host = str(Host)
                   DisCover = Popen(["ping", "-w1",Host], stdout=PIPE)
                   output   = DisCover.communicate()[0]
                   respons  = DisCover.returncode       
                   pid = Popen(["arp", "-a", Host], stdout=PIPE)
                   arp_host = pid.communicate()[0]                          
                   Mac_arp = str(arp_host)
                   Macaddr = re.compile(r'(?:[0-9a-fA-F]:?){12}')
                   Mac = str(re.findall(Macaddr ,Mac_arp)).replace("['",'').replace("']","")       	
                   MacGET= str("".join(Mac[0:8])).replace(":","").upper()
                   Macdb = open('Package/mac-vendor.txt', 'r')
                   MacFile = Macdb.readlines()
                   count = 0
                   for line in MacFile:
                       line = line.strip()
                       if MacGET in line  : 
                          vendor1 = line[7:].replace("    ","")  
                          break
                       elif MacGET not  in line:
                            vendor1 = " Unknown-MAC" 
                            count += 1  
                   if respons == 0:
                         if Host == host_ip and \
                           "no match found" in Mac_arp and str(ipaddress.ip_address(Host)) ==  str(ipaddress.ip_address(host_ip)) :
                                print(R+"|  "+Y+f"{Host:<23}",R+"|   "+Y+f"{Mac_Interface:<21}"+R+"|  "+Y+f"{vendor:<25}",R+"|") 
                                 
                                if self.args.output : 
                                    printF +="|  "+f"{Host:<23}"+"|   "+f"{Mac_Interface:<21}"+"|  "+f"{vendor:<27}"+"|"+'\n'                                                                  
                         elif "no match found" in Mac_arp and str(ipaddress.ip_address(Host)) != str(ipaddress.ip_address(host_ip)) :                     
                                print(R+"|  "+Y+f"{Host:<23}",R+"|"+P+f"{'   ------None-----    ':<23}"+R+" | "+B+f"{'  ------None----- ':<25}",R+" |")
                                
                                if self.args.output : 
                                   printF +=("|  "+f"{Host:<23}"+"|"+f"{'   ------None-----    ':<23}"+" | "+f"{'  ------None----- ':<26}"+"  |")+'\n'                                  
                         else:                    	                                                                             
                              print(R+"|  "+B+f"{Host:<23}",R+"|   "+P+f"{Mac:<21}"+R+"| "+W+f"{vendor1[0:23]:<25}"+R+"  |"+R)
                              if self.args.output :
                                 printF +=str("|  "+f"{Host:<23}"+"|   "+f"{Mac:<21}"+"| "+f"{vendor1[0:23]:<26}"+"  |")+'\n'
                   else:
                         
                           host_split = Host.split(".")                              
                           print(R+"|  "+Y+f"{Host:<23}",R+"|"+P+f"{'   00:00:00:00:00:00   ':<21}"+R+" | "+B+f"{'   HOST DONW          ':<26}",R+"|")
                   print(Banner)       
                   if self.args.output :          
                       with open("./Scan-Store/"+self.args.output,"w+") as out_put:
                          out_put.write(Banner1+'\n'+"\n"+printF) 
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
