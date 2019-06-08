# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Iscsi_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nnmap -n -sV --script=iscsi-info -p '+self.port+' '+ self.host, "shell": True, "chain": False},

        ]

        if self.intensity == "3":
            if username != "":
                self.cmds = [{"name": self.proto+"_brute_nmap_"+self.port, "cmd": 'nmap -sV --script iscsi-brute --script-args userdb='+self.username+',passdb='+self.plist+' -p ' + self.port + ' ' + self.host, "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": self.proto+"_brute_nmap_"+self.port, "cmd": 'nmap -sV --script iscsi-brute --script-args userdb='+self.ulist+',passdb='+self.plist+' -p ' + self.port + ' ' + self.host, "shell": True, "chain": False}]
