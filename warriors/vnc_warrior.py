# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Vnc_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n -sV --script vnc-info,realvnc-auth-bypass,vnc-title -p ' + self.port + ' ' + self.host, "shell": True,"chain": False},

        ]

        msfmodules = [
            {"path": "auxiliary/scanner/vnc/vnc_none_auth", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
        ]
        self.cmds.append(
            {"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -l '+self.username+' -P '+self.plist+' -s '+self.port+' '+self.host+' vnc', "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -L ' + self.ulist + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' vnc', "shell": True, "chain": False}]
