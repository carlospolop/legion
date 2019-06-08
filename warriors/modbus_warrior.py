# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#You can test this module against querier (10.10.10.125)

class Modbus_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap-n  --script modbus-discover -sV -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},

        ]

        msfmodules = [{"path": "auxiliary/scanner/scada/modbusdetect", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                      {"path": "auxiliary/scanner/scada/modbus_findunitid", "toset": {"RHOSTS": self.host, "RPORT": self.port}}
                      ]
        self.cmds.append({"name": self.modbus+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})
