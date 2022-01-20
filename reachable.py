#!/usr/bin/env python3

import argparse
import sys
from Package.Banner import *
import os
import subprocess

S='\033[0m' 
W = "\033[1;37m"
R = "\033[0;31m"
D = "\033[1m"
I = "\033[3m"
B = '\033[34m'  
Y='\033[1;33m'


class Run :
        print(Banner)
        def Check_InterFace(self):
            if self.args.Interface:
              try:
                  commad_ifconfig = "ifconfig | grep  "+ self.args.Interface
                  commad_ifconfig = subprocess.check_output (commad_ifconfig,shell=True).decode('utf-8')
              except Exception:
                     print(B+"\n[+] Device [ "+Y +self.args.Interface+B+ " ] does not exist \n")
                     print(W+D+I+"\n[*] Device available-\n"+R+"="*14+"\n")
                     all_Interface = os.listdir('/sys/class/net/') 
                     for i in all_Interface :
                          print(B+'[+] Interface : '+Y, i)
                     print()    
                     exit()                         
        def __init__(self):
            self.args_command() 
            self.Check_InterFace()
            self.control()
        def control(self):
           if self.args.Pnetwork and not self.args.start and not self.args.end :
              from Package.Pingclass import  Discover_Network
              print("--PING-SCAN"+"\n"+"+"*20)
              run = Discover_Network()
              exit()
           elif self.args.Pnetwork and  self.args.start and self.args.end :
              from Package.HostRange import RangeOfHosts
              print("--PING-SCAN"+"\n"+"+"*20)
              run = RangeOfHosts()
              exit()
           elif self.args.phost :
                 from Package.OneHost import  Host_One
                 print("--PING-SCAN"+"\n"+"+"*20)
                 run = Host_One()
                 exit()
           elif self.args.arpnetwork and not self.args.start and not self.args.end :
              from ARP_PACK.arp_class import Arp_Network
              print("--ARP-SCAN"+"\n"+"+"*20)
              run = Arp_Network()
              exit()
           elif self.args.arpnetwork and self.args.start and self.args.end and not self.args.Pnetwork :
              from ARP_PACK.arp_range import Range_arp_host
              print("--ARP-SCAN"+"\n"+"+"*20)
              run = Range_arp_host()
              exit()
           elif self.args.ahost :             
                 from ARP_PACK.arp_one_Host import  Arp_Host_One
                 print(B+"--ARP-SCAN"+"\n"+"+"*20)
                 run = Arp_Host_One()
                 exit()      
        def args_command(self):
              print(Y+"")
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser.add_argument( '-PN',"--Pnetwork"     ,metavar='' , action=None ,help ="ping all Network ,IPaddress/prefix ")
              parser.add_argument( '-AN',"--arpnetwork"   ,metavar='' , action=None ,help ="arp scan  all Network ,IPaddress/prefix ")
              parser.add_argument( '-O',"--output"        ,metavar='' , action=None  ,help ="output file report ")
              parser.add_argument( '-S',"--start"         ,metavar='' , action=None  ,help ="start of the range Ips ")
              parser.add_argument( '-PH',"--phost"          ,metavar='' , action=None  ,help ="Ping One Host Only ")
              parser.add_argument( '-AH',"--ahost"          ,metavar='' , action=None  ,help ="arp  One Host Only ")
              parser.add_argument( '-E',"--end"           ,metavar='' , action=None  ,help ="end of the range ips ")
              parser.add_argument( '-M',"--Mac"           ,metavar='' , action=None  ,help ="end of the range ips ")
              parser.add_argument( '-I',"--Interface"     ,metavar='' , action=None  ,help =" User Interface  ")
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   
                   pass
              else:
                   parser.print_help()
                   print(R+"="*15+S)
                   print(R+"-Example ping scan :-"+"\n"+"="*10+S)
                   print(Y+"-To Scan all Subnet Use -N <network/prefix>\n./reachable.py -N 10.195.100.200/25")               
                   print(R+"\t\t"+"="*20+'\n')
                   print(Y+"-To Scan range of ips Use -N <network/prefix> -S <Start>  -E <end>\n./reachable.py -N 10.195.100.200/24 -S 240 -E 254 ")               
                   print(R+"\t\t"+"="*20)
                   print(Y+"-To Scan one Host  Use  '-H' <host ip>\n./reachable.py -H 10.195.100.200/25\nor\n./reachable.py -H 10.196.100.3")
                   print(R+"\t\t"+"="*20)
                   print(Y+"-To Save the output into file Use -O <file name>")
                   print(Y+"./reachable.py -N 10.195.100.200/24 -S 240 -E 254 -O report.txt") 
                   print(R+"="*15)
                   print()
                   print(W+"[*] For arp Scan Use root Login or  sudo privileges ")
                   print(Y+" -I or --Interface  use ifconfig to make sure that any of the interface are available ") 
                   print(R+"-Example arp scan-:-\n"+"="*10)
                   print(Y+"-To Scan all Subnet Use -N <network/prefix> -I < Interface > \nsudo./reachable.py -N 10.195.100.200/25 -I eth0 ")               
                   print(R+"\t\t"+"="*20)
                   print(Y+"-To Scan range of ips Use -N <network/prefix> -S <Start>  -E <end>\nsudo./reachable.py -N 10.195.100.200/24  -I eth0 -S 240 -E 254 ")               
                   print(R+"\t\t"+"="*20)
                   print(Y+"-To Scan one Host  Use  '-H' <host ip>\n sudo ./reachable.py -H 10.195.100.200/25 -I eth0 \nor\n sudo./reachable.py -H 10.196.100.3 -I wlan0")
                   print(R+"\t\t"+"="*20)
                   print(Y+"-To Save the output into file Use -O <file name>")
                   print(Y+"sudo ./reachable.py -N 10.195.100.200/24  -I eth0 -S 240 -E 254 -O report.txt") 
                   print(Banner)
                   exit()

if __name__=="__main__":
   Run()
