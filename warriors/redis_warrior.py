# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

class Redis_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n --script redis-info -sV -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},
        ]

        msfmodules = [
            {"path": "auxiliary/scanner/redis/redis_server", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
        ]
        self.cmds.append(
            {"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity == "3":
            self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -P '+self.plist+' -s '+self.port+' '+self.host+' redis', "shell": True, "chain": False}]
