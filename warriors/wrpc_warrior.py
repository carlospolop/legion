# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#apt-get install rpcbind
#You can check this module with irked.htb (10.10.10.117)
#Soft link to rpcdump.py

class Wrpc_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_rpcdump", "cmd": 'python $(which rpcdump.py) -p 135 ' + self.host + " || echo 'rpcdump.py is not in path!'", "shell": True, "chain": False},
            {"name": self.proto+"_nmap_"+self.port, "cmd": "nmap -n -sV --script=msrpc-enum -p "+self.port+" "+self.host, "shell": True, "chain": False}
        ]

        msfmodules = [{"path": "scanner/dcerpc/endpoint_mapper", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                      {"path": "auxiliary/scanner/dcerpc/management", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                      {"path": "auxiliary/scanner/dcerpc/tcp_dcerpc_auditor", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                      {"path": "auxiliary/scanner/dcerpc/hidden", "toset": {"RHOSTS": self.host, "RPORT": self.port}}
                      ]

        self.cmds.append({"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

