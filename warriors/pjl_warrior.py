# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Pjl_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n -sV --script pjl-ready-message -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},

        ]

        msfmodules = [
            {"path": "auxiliary/scanner/printer/printer_env_vars", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            {"path": "auxiliary/scanner/printer/printer_list_dir", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            {"path": "auxiliary/scanner/printer/printer_list_volumes", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            {"path": "auxiliary/scanner/printer/printer_ready_message", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            {"path": "auxiliary/scanner/printer/printer_version_info", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            {"path": "auxiliary/scanner/printer/printer_version_info", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            {"path": "auxiliary/scanner/printer/printer_env_vars", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            {"path": "auxiliary/scanner/printer/printer_env_vars", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
        ]
        self.cmds.append(
            {"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})
