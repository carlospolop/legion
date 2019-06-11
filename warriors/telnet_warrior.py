# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Telnet_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": "telnet_nmap_"+self.port, "cmd": 'nmap -n -sV --script "telnet* and safe" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},
            {"name": "telnet_version_"+self.port, "cmd": 'nc -w 20 -q 1 -vn ' + self.host + ' ' + self.port + ' </dev/null', "shell": True, "chain": False},
        ]

        msfmodules = [{"path": "auxiliary/scanner/telnet/telnet_version", "toset": {"RHOSTS": self.host, "RPORT": self.port}}, ]
        self.cmds.append({"name": "telnet_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity >= "2":
            msfmodules_vulns = [
                                {"path": "auxiliary/scanner/telnet/brocade_enable_login", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                                {"path": "auxiliary/scanner/telnet/telnet_encrypt_overflow", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                                {"path": "auxiliary/scanner/telnet/telnet_ruggedcom", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                                ]
            self.cmds.append(
                {"name": "telnet_msf_vuln_"+self.port, "cmd": self.create_msf_cmd(msfmodules_vulns), "shell": True, "chain": False})

        if self.intensity == "3":
            if username != "":
                self.cmds = [{"name": "telnet_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -l ' + self.username + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' telnet', "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": "telnet_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -L ' + self.ulist + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' telnet', "shell": True, "chain": False}]

