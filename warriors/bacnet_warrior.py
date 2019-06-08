# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Bacnet_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n -sV --script bacnet-info --script-args full=yes -p '+self.port+' '+self.host, "shell": True, "chain": False},
        ]
