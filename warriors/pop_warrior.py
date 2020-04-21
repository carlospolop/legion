# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Pop_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto + "_nmap_"+self.port, "cmd": 'nmap -n --scripts "pop3-capabilities or pop3-ntlm-info" -sV -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},

        ]

        if self.proto == "pop":
            self.cmds.append({"name": self.proto + "_version_"+self.port, "cmd": 'nc -w 20 -q 1 -vn ' + self.host + ' ' + self.port + ' </dev/null', "shell": True, "chain": False})
        else:
            self.cmds.append({"name": self.proto + "_version_"+self.port, "cmd": 'echo QUIT | openssl s_client -connect '+self.host+':'+self.port+' -crlf -quiet', "shell": True, "chain": False})


        msfmodules = [{"path": "auxiliary/scanner/pop3/pop3_version", "toset": {"RHOSTS": self.host, "RPORT": self.port}}]

        self.cmds.append({"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            ssl = " -S " if self.proto == "pops" else ""  # Check if SSL is needed
            if username != "":
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -l '+self.username+' -P '+self.plist+ ssl +' -s '+self.port+' '+self.host+' pop3', "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -L ' + self.ulist + ' -P '+self.plist+ ssl +' -s ' + self.port + ' ' + self.host + ' pop3', "shell": True, "chain": False}]

