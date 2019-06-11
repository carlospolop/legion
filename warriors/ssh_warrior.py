# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

class Ssh_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": "ssh_nmap_"+self.port, "cmd": 'nmap -n -sV --script "ssh-auth-methods or ssh-auth-methods or ssh2-enum-algos or sshv1" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},
            {"name": "ssh_sslscan_"+self.port, "cmd": "sslscan "+self.host_port, "shell": False, "chain": False},
            {"name": "ssh_sslyze_"+self.port, "cmd": "sslyze --regular "+self.host_port, "shell": False, "chain": False},
            {"name": "ssh_version_"+self.port, "cmd": 'nc -w 20 -q 1 -vn ' + self.host + ' ' + self.port+ ' </dev/null', "shell": True, "chain": False},
        ]

        msfmodules = [{"path": "auxiliary/scanner/ssh/ssh_version", "toset": {"RHOSTS": self.host, "RPORT": self.port}}]
        self.cmds.append({"name": "ssh_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity >= "2":
            msfmodules_vulns = [{"path": "scanner/ssh/ssh_enumusers", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USER_FILE": self.ulist}},
                                {"path": "auxiliary/scanner/ssh/juniper_backdoor", "toset": {"RHOSTS": self.host, "RPORT": self.port}}]
            self.cmds.append({"name": "ssh_msf_vuln_"+self.port, "cmd": self.create_msf_cmd(msfmodules_vulns), "shell": True, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                self.cmds = [{"name": "ssh_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -l ' + self.username + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' ssh', "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": "ssh_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -L ' + self.ulist + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' ssh', "shell": True, "chain": False}]

