# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Saprouter_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        msfmodules = [
            {"path": "auxiliary/scanner/sap/sap_service_discovery", "toset": {"RHOSTS": self.host}},
            {"path": "auxiliary/scanner/sap/sap_router_info_request", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            ]
        self.cmds.append({"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})
