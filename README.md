# reachable:-
*****************************
### reachable network scan
* reachable its tool writen with pyhton3 hele to discover the hosts devices on the Network .
* reachable tool have two ways to get the host on network Ping scan and arp scan. 
* by star reachable will grep  you host info and your netwok subnet
### ping Scan -
===============
 - Ping scan by sending Internet Control Message Protocol (ICMP) echo request packets to the target host and waiting for an ICMP echo reply. 
 - user can ping all network subnet or rangs of ips or one host
 - reachable tool will get the mac-addess for davice and mac-vendor as well 
* code dowblow the part of respones about gentrat the hostip for all subnet mask then sen echo ping recqut one by one then wating for repones 
and use rexuxe to mach the mac address and print the mac-adrees and mac-vendor 
 ```python 
 for Host in Network .hosts():
           Host = str(Host)
           DisCover = Popen(["ping", "-w1",Host], stdout=PIPE)
           output   = DisCover.communicate()[0]
           respons  = DisCover.returncode                       
           if respons == 0:
               Hcount  +=1	
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
                   if "no match found" in Mac_arp and str(ipaddress.ip_address(Host)) ==  str(ipaddress.ip_address(host_ip)) :
                          print(Y+D+I+"[*] Mac-Address     ..............|-",Mac_Interface)
                          if self.args.output :
                                 printF = str("[*] Mac-Address     ..............|- "+Mac_Interface).strip()
                                 with open (self.args.output,'a') as out_put :
                                      out_put.write(str(printF+"\n"))
                          interfaceMac = Mac_Interface[0:8].replace(":","").upper() 
 ```
 <img src = "images/2.png" width=450>  <img src = "images/1.png" width=450>

 ===========================================================================================

 ## arp Scan - 
 ===============
 
