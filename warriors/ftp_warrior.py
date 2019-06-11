# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Ftp_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": "ftp_nmap_"+self.port, "cmd": 'nmap -n -sV --script "ftp* and default" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},
            {"name": "ftp_version_"+self.port, "cmd": 'nc -w 20 -q 1 -vn ' + self.host + ' ' + self.port + ' </dev/null', "shell": True, "chain": False},

        ]

        msfmodules = [{"path": "auxiliary/scanner/ftp/anonymous", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                      {"path": "auxiliary/scanner/ftp/ftp_version", "toset": {"RHOSTS": self.host, "RPORT": self.port}},]

        self.cmds.append({"name": "ftp_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity >= "2":
            self.cmds.append({"name": "ftp_nmap_vuln_"+self.port, "cmd": 'nmap -sV --script "ftp* and vuln" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False})
            msfmodules_vuln = [
                {"path": "auxiliary/scanner/ftp/bison_ftp_traversal", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                {"path": "auxiliary/scanner/ftp/colorado_ftp_traversal", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                {"path": "auxiliary/scanner/ftp/easy_file_sharing_ftp", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                {"path": "auxiliary/scanner/ftp/konica_ftp_traversal", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                {"path": "auxiliary/scanner/ftp/pcman_ftp_traversal", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                {"path": "auxiliary/scanner/ftp/titanftp_xcrc_traversal", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            ]
            self.cmds.append({"name": "ftp_msf_vuln_"+self.port, "cmd": self.create_msf_cmd(msfmodules_vuln), "shell": True, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                self.cmds = [{"name": "ftp_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -l '+self.username+' -P '+self.plist+' -s '+self.port+' '+self.host+' ftp', "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": "ftp_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -L ' + self.ulist + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' ftp',"shell": True, "chain": False}]
