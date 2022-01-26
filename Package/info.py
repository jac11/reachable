#!/usr/bin/env python3 

from Package.Banner import *
S='\033[0m' 
W = "\033[1;37m"
R = "\033[0;31m"
D = "\033[1m"
I = "\033[3m"
B = '\033[34m'  
Y='\033[1;33m'

class Info_print:

  
       print(Banner)
       a = W+   '''
              ##################################################
             #                                                  #
             #                    reachable                     #
             #                  NetWork-Scan                    #
             #                ping-scan/arp-scan                #                                          
             #          author   : jacstory                     #
             #          email    : rootx1982@gmail.com          #
             #          GitHub   : https://github.com/jac11     #
             #          version  : 10.0.1                       #
             #          language  : python3.9                   #
             #                                                  #
              ##################################################    
             
       '''+S
       print(a)
       print(R+"="*15+S)
       print(R+"-Example ping scan :-"+"\n"+"="*10+S)
       print(Y+"-To Scan all Subnet Use -PN <network/prefix> -I <Interface>\n./reachable.py -PN 10.195.100.200/25 -I eth0")              
       print(R+"\t\t"+"="*20+'\n')
       print(Y+"-To Scan range of ips Use -PN <network/prefix> -S <Start>  -E <end> -I <Interface>\n./reachable.py -PN 10.195.100.200/24 -S 240 -E 254 -I eth0 ")             
       print(R+"\t\t"+"="*20)       
       print(Y+"-To Scan one Host  Use  '-PH' <host ip> -I <Interface>\n./reachable.py -PH 10.195.100.200/25 -I eth0\nor\n./reachable.py -PH 10.196.100.3 -I eth0 ")
       print(R+"\t\t"+"="*20)
       print(Y+"-To Save the output into file Use -O <file name>")
       print(Y+"./reachable.py -PN 10.195.100.200/24 -I eth0 -S 240 -E 254 -O report.txt") 
       print(R+"="*15)
       print()
       print(W+'PING SCAN WITH CHANGE MAC')
       print(W+"For Scan with change host mac Use root Login or  sudo privileges ")
       print(W+"if the interface ip address  with 'DHCP' your ip addrss with chane as well")
       print(W+"after scan finish the Mac address  and the ip set  to real mac and previous ip \n")
       print(R+"="*15)
       print()
       print(Y+"-To Scan all Subnet  and chamge Host Mac Use -PN  <network/prefix> -I <Interface>  -M <true>\nsudo ./reachable.py -PN 10.195.100.200/25 -I eth0 -M true")               
       print(R+"\t\t"+"="*20+'\n')
       print(Y+"-To Scan range of ips  and Change Host Mac Use -PN <network/prefix> -S <Start>  -E <end> -I < interface> -M < true>\
       \n./reachable.py -PN 10.195.100.200/24 -S 240 -E 254  -I eth0 -M true")               
       print(R+"\t\t"+"="*20)
       print(R+"="*15)
       print()
       print(R+"-Example arp scan :-"+"\n"+"="*10+S)
       print(W+"For arp Scan Use root Login or  sudo privileges ")
       print(W+"To use  -I or --Interface  use ifconfig to make sure that any of the interface are available ") 
       print(Y+"-To Scan all Subnet Use -AN <network/prefix> -I < Interface > \nsudo./reachable.py -AN 10.195.100.200/25 -I eth0 ")               
       print(R+"\t\t"+"="*20)
       print(Y+"-To Scan range of ips Use -AN <network/prefix> -S <Start>  -E <end>\nsudo./reachable.py -AN 10.195.100.200/24  -I eth0 -S 240 -E 254 ")               
       print(R+"\t\t"+"="*20)
       print(Y+"-To Scan one Host  Use  '-AH' <host ip>\n sudo ./reachable.py -AH 10.195.100.200/25 -I eth0 \nor\n sudo./reachable.py -H 10.196.100.3 -I wlan0")
       print(R+"\t\t"+"="*20)
       print(Y+"-To Save the output into file Use -O <file name>")
       print(Y+"sudo ./reachable.py -AN 10.195.100.200/24  -I eth0 -S 240 -E 254 -O report.txt") 
       print()
       print(W+'PING SCAN WITH CHANGE MAC')
       print(R+"="*15)
       print(Y+"-To Scan all Subnet  and chamge Host Mac Use -AN  <network/prefix> -I <Interface>  -M <true>\nsudo ./reachable.py -PN 10.195.100.200/25 -I eth0 -M true")               
       print(R+"\t\t"+"="*20+'\n')
       print(Y+"-To scan range of ips  and Change Host Mac Use -PN <network/prefix> -S <Start>  -E <end> -I < interface> -M < true>\
       \nsudo ./reachable.py -PN 10.195.100.200/24 -S 240 -E 254  -I eth0 -M true") 
       print(Banner)
if __name__=='__main__':
    Info_print()
