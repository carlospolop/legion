# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

# https://github.com/portcullislabs/udp-proto-scanner.git copy the conf file to bin also

#You can test this module against sizzle.htb (10.10.10.103)
#Or against conceal.htb(10.10.10.116)  (hidden snmp detected by udp-proto-scanner)

class Scanner_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)
        self.workdir = self.workdir + "/../"

        if self.ip != "":
            self.cmds = [{"name": "udp-proto-scanner", "cmd": 'udp-proto-scanner.pl ' + self.ip, "shell": False, "chain": False}]

        self.cmds += [
            {"name": "nmap_fast_udp", "cmd": 'nmap -F -sU -sV -T 4 -oA '+self.workdir+'nmapu '+ self.host, "shell": False, "chain": False},
            {"name": "nmap_init", "cmd": 'nmap -sS -sV -T 4 -oA '+self.workdir+'nmapi ' + self.host, "shell": False, "chain": True},
            {"name": "nmap_full_fast", "cmd": 'nmap -sS -sV -sC -O -T 4 -p - -oA '+self.workdir+'nmapff ' + self.host, "shell": False, "chain": True},
            {"name": "nmap_full", "cmd": 'nmap -sS -sV -sC -O -p - -oA '+self.workdir+'nmapf ' + self.host, "shell": False, "chain": True},
            {"name": "nmap_sctp_full", "cmd": 'nmap -T 4 -sY -sV -sC -p - -oA '+self.workdir+'nmapfsctp ' + self.host, "shell": False, "chain": False},
            #{"name": "nmap_udp_full", "cmd": 'nmap -sU -sV -p - ' + self.host, "shell": False, "chain": False}
        ]

