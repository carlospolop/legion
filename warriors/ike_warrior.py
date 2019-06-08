# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#https://github.com/SpiderLabs/ikeforce
#symlink
#You can test this against conceal.htb (10.10.10.116)

class Ike_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)
        self.password = self.password if len(self.password)>0 else "vpn"

        self.extra_info += "\nIf nothing is set in variable 'password' this module will use 'vpn' as ID."

        self.cmds = [
            {"name": "ike_nmap", "cmd": 'nmap -n -sV --script *ike* -sU -p ' + self.port + ' ' + self.host, "shell": False, "chain": False},
            {"name": "ike-scan", "cmd": 'ike-scan -M --sport '+self.port+' --dport '+self.port+' '+ self.host, "shell": False, "chain": True},
            {"name": "ike-scan_nat", "cmd": 'ike-scan -M --nat-t ' + self.host, "shell": False, "chain": True},
            {"name": "ike-scan_showback", "cmd": 'ike-scan -M --showbackoff --sport '+self.port+' --dport '+self.port+' ' + self.host,
             "shell": False, "chain": True},
            {"name": "ike-scan_agressive",
             "cmd": 'ike-scan --aggressive --id=' + self.password + ' --sport '+self.port+' --dport '+self.port+' '+self.host,
             "shell": False, "chain": True},
            {"name": "ike-scan_agr_psk",
             "cmd": 'ike-scan --pskcrack --aggressive --id='+self.password+' --sport '+self.port+' --dport '+self.port+' '+ self.host,
             "shell": False, "chain": True},
        ]

        if self.intensity == "3":
            self.extra_info = "To bruteforce IKE an 'ip' must be set."
            if self.ip != "":
                self.plist = self.plist if self.plist != "" else self.wordlists_path+'/wordlists/groupnames.txt'
                self.cmds.append({"name": "ikeforce_id", "cmd": 'ikeforce '+self.ip+' -e -w '+self.plist+' -s 2', "shell": False, "chain": True})
            # TODO: Bruteforce XAUTH and transformations (the 500 port is needed so the bruteforce has to be concatenated)
