# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Ajp_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto + "_nmap_"+self.port, "cmd": 'nmap -n -sV --script ajp-auth,ajp-headers,ajp-methods,ajp-request -sV -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},

        ]

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                self.cmds = [{"name": self.proto+"_brute_nmap_"+self.port, "cmd": 'nmap -n -sV --script ajp-brute --script-args userdb='+self.username+',passdb='+self.plist+' -p '+self.port+' '+self.host, "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": self.proto+"_brute_nmap_"+self.port, "cmd": 'nmap -n -sV --script ajp-brute --script-args userdb='+self.ulist+',passdb='+self.plist+' -p '+self.port+' '+self.host, "shell": True, "chain": False}]

