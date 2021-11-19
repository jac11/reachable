#!/usr/bin/env python3 

import argparse
import sys
from Package.Banner import *
 

class Run :
        print(Banner)
        def __init__(self):
            self.args_command()  
            self.control()
        def control(self):
           if self.args.network and not self.args.start and not self.args.end and not self.args.Interface:
             
              from Package.Pingclass import  Discover_Network
              print("\t\t\t      PING-SCAN"+"\n\t\t        "+"+"*20+"\n")
              run = Discover_Network()
              exit()
           elif self.args.start and self.args.end and not self.rgs.Interface and not self.args.Interface:
              
              from Package.HostRange import RangeOfHosts
              print("\t\t\t      PING-SCAN"+"\n\t\t        "+"+"*20+"\n")
              run = RangeOfHosts()
              exit()
           elif self.args.Host and not self.args.Interface:
              
                 from Package.OneHost import  Host_One
                 print("\t\t\t      PING-SCAN"+"\n\t\t        "+"+"*20+"\n")
                 run = Host_One()
                 exit()
           elif self.args.network and not self.args.start and not self.args.end and self.args.Interface:
             
              from ARP_PACK.arp_class import Arp_Network
              print("\t\t\t      ARP-SCAN"+"\n\t\t        "+"+"*20+"\n")
              run = Arp_Network()
              exit()
           elif self.args.start and self.args.end and self.args.Interface :
              
              from ARP_PACK.arp_range import Arp_Host_One
              print("\t\t\t      ARP-SCAN"+"\n\t\t        "+"+"*20+"\n")
              run = Arp_Host_One()
              exit()
           elif self.args.Host and self.args.Interface:
              
                 from ARP_PACK.arp_one_Host import  Arp_Host_One
                 print(B+"\t\t\t      ARP-SCAN"+"\n\t\t        "+"+"*20+"\n")
                 run = Arp_Host_One()
                 exit()      
        def args_command(self):
              parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
              parser.add_argument( '-N',"--network"   ,metavar='' , action=None ,help ="ping all Network ,IPaddress/prefix ")
              parser.add_argument( '-O',"--output"    ,metavar='' , action=None  ,help ="output file report ")
              parser.add_argument( '-S',"--start"     ,metavar='' , action=None  ,help ="start of the range Ips ")
              parser.add_argument( '-H',"--Host"      ,metavar='' , action=None  ,help ="Ping One Host Only ")
              parser.add_argument( '-E',"--end"       ,metavar='' , action=None  ,help ="end of the range ips ")
              parser.add_argument( '-I',"--Interface"       ,metavar='' , action=None  ,help ="Interface use for arp scan ")
              self.args = parser.parse_args()
              if len(sys.argv)> 1 :
                   
                   pass
              else:
                   parser.print_help()
                   print(R+"="*15)
                   print("Example:-"+"\n"+"="*10)
                   print("-To Scan all Subnet Use -N <network/prefix>\n./Pingalbe.py -N 10.195.100.200/25")               
                   print("\t\t"+"="*20)
                   print("-To Scan range of ips Use -N <network/prefix> -S <Start>  -E <end>\n./Pingalbe.py -N 10.195.100.200/24 -S 240 -E 254 ")               
                   print("\t\t"+"="*20)
                   print("-To Scan one Host  Use  '-H' <host ip>\n./Pingalbe.py -H 10.195.100.200/25 \nor\n./pingable.py -H 10.196.100.3")
                   print("\t\t"+"="*20)
                   print("-To Save the output into file Use -O <file name>")
                   print("./Pingalbe -N 10.195.100.200/24 -S 240 -E 254 -O report.txt") 
                   print(Banner)
                   exit()

if __name__=="__main__":
   Run()

