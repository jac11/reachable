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
 
 
S='\033[0m' 
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
                   Network     = ipaddress.ip_network('{}'.format(self.args.network), strict=False)
                   Network_ID  = Network.network_address
                   SubNet      = Network.netmask
                   Hosts_range = Network.num_addresses - 2 
                   end_ip = str(Network.broadcast_address).split('.')
                   scop   = "/"
                   try :
                       NetworkID = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.network[-2:])) 
                   except Exception :
                        NetworkID = ipaddress.ip_network('{}{}{}'.format(Network_ID,scop,self.args.network[-1:]))
                   fix  = self.args.network
                   ip,sub = fix.split('/')
                   oct_ip = ip.split('.')
                   start_ip = str(Network_ID).split(".") 
                   if (int(self.args.start)==int(start_ip[3])):
                           print(R+"\n"+"="*50+"\n"+"[+] Erorr       --------------|- Start Ip is Netwotk-ID "+"\n"+"="*50+"\n")
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
                   total = int(self.args.end) - int(self.args.start) 
                   print(W+D+I+"\n[*] HOST INFO-\n"+R+"="*17+"\n")
                   print(B+D+I+"[+] HOST-IP         --------------|- " +  host_ip)
                   print("[+] Mac-Address     --------------|- " +  Mac_Interface)
                   print("[+] Mac-Vendor      --------------|- " + vendor)
                   print(W+D+I+"\n[*] NETWORK INFO-\n"+R+"="*17+"\n")
                   print(B+D+I+"[+] Network-ID      --------------|- " +  str(Network_ID))
                   if "/" in self.args.network[-2:] :
                        print("[+] NetWork-Prefix  --------------|- " +  self.args.network[-1:])
                   else:
                       print("[+] NetWork-Prefix  --------------|- " +  self.args.network[-2:])
                   print("[+] Subnet-Mask     --------------|- " +  str(SubNet))
                   print("[+] Frist ip        --------------|- " +  str([ x for x in Network.hosts()][0]))
                   print("[+] Last ip         --------------|- " +  str([ x for  x  in  Network.hosts()][-1]))
                   print("[+] Number of hosts --------------|- " +  str(Hosts_range ))
                   print("[+] Broadcast IP    --------------|- " +  str(Network.broadcast_address))
                   print(W+D+I+"\n[*] Range Host -\n"+R+"="*17)
                   print(B+I+D+"[+] Start-Count     --------------|- " + self.args.start)
                   print(B+D+I+"[+] End-Count       --------------|- " + self.args.end)
                   print(B+D+I+"[+] Host-Count      --------------|- " + str(total ))
                   print(R+"\n"+"="*50+"\n"+W+D+I+"[*] Host-discover-"+"\n"+R+"="*20+"\n")
                   if self.args.output:
                         printF  = ""
                         printF  += ("[+] "+ command_argv)+"\n"
                         printF  += ("\n[*] HOST INFO-\n"+"="*17+"\n")+"\n"
                         printF  += ("[+] HOST-IP         --------------|- " +  host_ip)+"\n"
                         printF  += ("[+] Mac-Address     --------------|- " +  Mac_Interface)+"\n"
                         printF  += ("[+] Mac-Vendor      --------------|- " + vendor)+"\n"
                         printF  += ("\n[*] NETWIRK INFO-\n"+"="*17+"\n")+"\n"
                         printF  += ("[+] Network-ID      --------------|- " +  str(Network_ID))+"\n"
                         if "/"in self.args.network[-2:]:
                              printF  += ("[+] NetWork-Prefix  --------------|- " +  self.args.network[-1:])+"\n"
                         else:
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
                        DisCover = Popen(["ping", "-w1",Host],stdout=PIPE,stderr=subprocess.PIPE)
                        output   = DisCover.communicate()[0]
                        respons  = DisCover.returncode                       
                        if respons == 0:
                            Hcount +=1
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
                            
                            if "no match found" in Mac_arp  and host_ip == Host :
                                  
                                 print(Y+D+I+"[*] Mac-Address     ..............|-",Mac_Interface)
                                 if self.args.output :
                                       printF = str("[*] Mac-Address     ..............|- "+Mac_Interface).strip()
                                       with open (self.args.output,'a') as out_put :
                                             out_put.write(str(printF+"\n"))
                                 interfaceMac = Mac_Interface[0:8].replace(":","").upper()
                                 
                            elif "no match found" in Mac_arp and Host != host_ip :
                                  print(B+W+I+"[*] Mac-Address     ..............|- None")
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
                            MacGET= Mac[0:8].replace(":","").upper()
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
                                
                            if "no match found" in Mac_arp  and host_ip == Host :
                                  print(Y+D+I+"[+] Mac-Vendor      --------------|  " +vendor)
                                  if  self.args.output :
                                      printF = str("[+] Mac-Vendor      --------------|  " +vendor).strip()
                                      with open(self.args.output ,"a") as out_put :
                                         out_put.write(str(printF+"\n"))
                                    
                            elif "no match found" in Mac_arp  and host_ip != Host :
                                  print(D+I+B+"[+] Mac-Vendor      --------------|  None ")
                                  if  self.args.output :
                                      printF = str("[+] Mac-Vendor      --------------|  None")
                                      with open(self.args.output ,"a") as out_put :
                                          out_put.write(str(printF+"\n"))
                            else: 
                                  print(B+D+I+"[+] Mac-Vendor      --------------| " +vendor1)
                                  if self.args.output :    
                                      printF = str("[+] Mac-Vendor      --------------| " +vendor1).strip()
                                      with open(self.args.output ,"a") as out_put :
                                          out_put.write(str(printF+"\n"))           
                            print()
                            if self.args.output:
                                  with open(self.args.output,"a") as out_put :
                                      out_put.write("\n")
                        else:
                            dcount +=1
                            print(D+Y+I+"[+] TRY HOST        --------------| ",Host)
                            sys.stdout.write('\x1b[1A')
                            sys.stdout.write('\x1b[2K')
                           
                   print(B+D+I+"\n[*] Scan-Result-\n"+R+"="*17+"\n")
                   print(B+D+I+"[+] Total-Hosts      --------------|-"+S+Y,str(total )),S
                   print(B+D+I+"[+] Active Hosts     --------------|-"+S+Y,str(Hcount)),S
                   if dcount == 0:
                       print(B+D+I+"[+] Inactive Hosts   --------------|-"+S+Y,str(total)),S
                   else:
                       print(B+D+I+"[+] Inactive Hosts   --------------|-"+S+Y,str(dcount)),S   
                   stop     = timeit.default_timer()
                   sec      = stop  - start
                   fix_time = time.gmtime(sec)
                   result   = time.strftime("%H:%M:%S",fix_time)  
                   print(B+D+I+"[+] Run-Time         --------------|- "+S+Y+result),S 
                    
                   print(Banner) 
                   if self.args.output:
                        printF   = ""
                        printF  += ("\n[*] Scan-Result-\n"+"="*17+"\n")+"\n"
                        printF  += ("[+] Total-Hosts     --------------|- " +  str(total ))+"\n"
                        printF  += ("[+] Active Hosts    --------------|- " +  str(Hcount))+"\n"  
                        if dcount == 0 :
                             printF  += ("[+] Inactive Hosts  --------------|- " +  str(total))+"\n"
                             printF  += ("[+] Run-Time        --------------|- " +  str(result))+"\n"
                        else:
                             printF  += ("[+] Inactive Hosts  --------------|- " +  str(dcount))+"\n"
                             printF  += ("[+] Run-Time        --------------|- " +  str(result))+"\n"
                        with open(self.args.output,'a') as out_put :
                             out_put.write(printF+Banner)
                   
             except Exception:
                  print(R+"\n"+"="*50+"\n"+W+I+D+"[*] HOST (",self.args.network,")   -------------| ValueError"+R+"\n"+"="*50+"\n")
             except KeyboardInterrupt:
                  print(Banner)
                  if self.args.output:
                      with open(self.args.output,'a') as out_put :
                           out_put.write(Banner)
      def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser.add_argument( '-N',"--network"   ,metavar='' , action=None ) 
              parser.add_argument( '-S',"--start"   ,metavar='' , action=None )
              parser.add_argument( '-O',"--output"   ,metavar='' , action=None)
              parser.add_argument( '-E',"--end"   ,metavar='' , action=None  )
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   pass
              else:
                   parser.print_help()
                   exit()                                        
       
if __name__=="__main__":
   RangeOfHosts()
  
