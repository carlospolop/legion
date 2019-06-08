# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Rsync_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -sV -n --script "rsync-list-modules" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},
        ]

        msfmodules = [{"path": "auxiliary/scanner/rsync/modules_list", "toset": {"RHOSTS": self.host, "RPORT": self.port}}]
        self.cmds.append({"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity == "3":  # TODO: add bruteforce only for 1 user
            self.cmds.append({"name": self.proto+"_brute_nmap_"+self.port, "cmd": 'nmap -sV --script rsync-brute --script-args userdb='+self.ulist+',passdb='+self.plist+' -p '+self.port+' '+self.host, "shell": True, "chain": False})

