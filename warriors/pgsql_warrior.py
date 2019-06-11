# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Pgsql_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_version_"+self.port, "cmd": 'nc -w 20 -q 1 -vn ' + self.host + ' ' + self.port + ' </dev/null', "shell": True,"chain": False},

        ]

        msfmodules = [
            {"path": "auxiliary/scanner/postgres/postgres_version", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
            {"path": "auxiliary/scanner/postgres/postgres_dbname_flag_injection", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
        ]
        self.cmds.append(
            {"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        #Database name param needed
        #if self.intensity >= "2":
        #    if self.username != "" and self.username[-1] != ">" and self.password != "" and self.password[-1] != ">":
        #        msfmodules_auth = [
        #            {"path": "auxiliary/scanner/postgres/postgres_hashdump", "toset": {"RHOSTS": self.host, "RPORT": self.port, "DATABASE": self.databasetodo, "USERNAME": self.username, "PASSWORD": self.password}},
        #            {"path": "auxiliary/scanner/postgres/postgres_schemadump", "toset": {"RHOSTS": self.host, "RPORT": self.port, "DATABASE": self.databasetodo, "USERNAME": self.username, "PASSWORD": self.password}},
        #            {"path": "auxiliary/admin/postgres/postgres_readfile", "toset": {"RHOSTS": self.host, "RPORT": self.port, "DATABASE": self.databasetodo, "USERNAME": self.username, "PASSWORD": self.password}},
        #            ]
        #        self.cmds.append({"name": "pgsql_msf_auth_"+self.port, "cmd": self.create_msf_cmd(msfmodules_auth), "shell": True, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -l '+self.username+' -P '+self.plist+' -s '+self.port+' '+self.host+' postgres', "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -L ' + self.ulist + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' postgres', "shell": True, "chain": False}]
