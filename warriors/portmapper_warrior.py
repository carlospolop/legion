# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#You can check this module with irked.htb (10.10.10.117)

class Portmapper_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)


        self.cmds = [
            {"name": "rpcinfo", "cmd": 'rpcinfo ' + self.host, "shell": False, "chain": False},
            {"name": "rpc_nfs_nmap_"+self.port, "cmd": 'nmap -n -sV --script "nfs-ls or nfs-showmount or nfs-statfs" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},
            {"name": self.proto+"_showmount", "cmd": 'showmount -e ' + self.host, "shell": True, "chain": False},
        ]

        msfmodules = [{"path": "auxiliary/scanner/nfs/nfsmount", "toset": {"RHOSTS": self.host, "RPORT": self.port}}]
        self.cmds.append({"name": self.proto + "_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})
