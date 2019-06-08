# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Afp_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n -sV --script "afp-* and not dos and not brute" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},

        ]

        msfmodules = [{"path": "auxiliary/scanner/afp/afp_server_info", "toset": {"RHOSTS": self.host, "RPORT": self.port}}]

        self.cmds.append({"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                msfmodules_brute = [{"path": "auxiliary/scanner/afp/afp_login", "toset": {"RHOSTS": self.host, "RPORT": self.port, "BLANK_PASSWORDS": "true", "USER_AS_PASS": "true", "PASS_FILE": self.plist, "USERNAME": self.username}}]
            else:
                msfmodules_brute = [{"path": "auxiliary/scanner/afp/afp_login", "toset": {"RHOSTS": self.host, "RPORT": self.port, "BLANK_PASSWORDS": "true", "USER_AS_PASS": "true", "PASS_FILE": self.plist, "USER_FILE": self.ulist}}]
            self.cmds = [{"name": self.proto+"_brute_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules_brute), "shell": True, "chain": False}]

