# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

class Oracle_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)
        self.sids = plist if len(plist) > 0 else self.wordlists_path+'/sids-oracle.txt'

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n --script "oracle-tns-version" -T4 -sV -p '+ self.port + ' ' + self.host, "shell": True, "chain": False},
            {"name": self.proto+"_tnscmd10g_version_"+self.port, "cmd": 'tnscmd10g version -p '+ self.port +' -h '+ self.host, "shell": False, "chain": False},
            {"name": self.proto+"_tnscmd10g_status_"+self.port, "cmd": 'tnscmd10g status -p '+ self.port +' -h '+ self.host, "shell": False, "chain": False},
            {"name": self.proto+"_oscanner_"+self.port, "cmd": 'oscanner -p '+ self.port +' -s '+ self.host, "shell": False, "chain": False},
            {"name": self.proto+"_odat_all_"+self.port, "cmd": 'odat.py all -p '+ self.port +' -s '+ self.host, "shell": False, "chain": False},
            {"name": self.proto+"_hydra_sids_"+self.port, "cmd": 'hydra -f -L '+self.sids+' -s '+self.port+' '+self.host+' oracle-sid', "shell": False, "chain": False},
            
        ]

        if self.intensity >= "2":
            self.extra_info = "Set the SID that you want to brute force in the 'username' option"
            if username != "":
                self.cmds.append({"name": self.proto+"_brute_nmap_"+self.port, "cmd": 'nmap -sV --script oracle-brute-stealth --script-args oracle-brute-stealth.sid='+self.username+' -p '+ self.port + ' ' + self.host, "shell": True, "chain": False},)

        #TODO: Add user/password bruteforce (not enough variables: SID, username, password)
        #All the checks that can perform metasploit are already made

