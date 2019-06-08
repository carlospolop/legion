# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Finger_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_cmd", "cmd": 'finger @' + self.host, "shell": True, "chain": False},
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n -sV --script finger -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},
        ]

        msfmodules = [{"path": "auxiliary/scanner/finger/finger_users", "toset": {"RHOSTS": self.host, "RPORT": self.port}}]
        self.cmds.append({"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity >= "2":
            self.cmds.append({"name": self.proto+"_execution", "cmd": 'finger "|/bin/id@' + self.host+'"', "shell": True, "chain": False})
