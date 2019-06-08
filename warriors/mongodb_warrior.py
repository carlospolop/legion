# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Mongodb_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": "mongodb_nmap_"+self.port, "cmd": 'nmap -n -sV --script "mongo* and default" -p '+self.port+' '+self.host, "shell": True, "chain": False},
        ]


        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                msfmodules_brute = [{"path": "auxiliary/scanner/mongodb/mongodb_login", "toset": {"RHOSTS": self.host, "RPORT": self.port, "BLANK_PASSWORDS": "true", "USER_AS_PASS": "true", "USERNAME":self.username, "PASS_FILE": self.plist}}]
            else:
                msfmodules_brute = [{"path": "auxiliary/scanner/mongodb/mongodb_login", "toset": {"RHOSTS": self.host, "RPORT": self.port, "BLANK_PASSWORDS": "true", "USER_AS_PASS": "true", "USER_FILE": self.username, "PASS_FILE": self.plist}},]
            self.cmds = [{"name": "mongodb_brute_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules_brute), "shell": True, "chain": False}]
