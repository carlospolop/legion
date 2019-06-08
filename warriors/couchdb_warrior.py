# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Couchdb_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_version_"+self.port, "cmd": 'curl http://' + self.host_port+'/', "shell": True, "chain": False},
            {"name": self.proto+"_dbs_"+self.port, "cmd": 'curl http://' + self.host_port+'/_all_dbs', "shell": True, "chain": False},
        ]

        msfmodules = [
            {"path": "auxiliary/scanner/couchdb/couchdb_enum", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
        ]
        self.cmds.append(
            {"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity >= "2":
            if self.username != "" and self.password != "":
                msfmodules_auth = [
                    {"path": "auxiliary/scanner/couchdb/couchdb_enum", "toset": {"RHOSTS": self.host, "RPORT": self.port, "HttpUsername": self.username, "HttpPassword": self.password}},
                    ]
                self.cmds.append({"name": self.proto+"_msf_auth_"+self.port, "cmd": self.create_msf_cmd(msfmodules_auth), "shell": True, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                msfmodules_brute = [{"path": "auxiliary/scanner/couchdb/couchdb_login", "toset": {"RHOSTS": self.host, "RPORT": self.port, "BLANK_PASSWORDS": "true", "USER_AS_PASS": "true", "USERNAME":self.username, "PASS_FILE": self.plist}},]
            else:
                msfmodules_brute = [{"path": "auxiliary/scanner/couchdb/couchdb_login", "toset": {"RHOSTS": self.host, "RPORT": self.port, "BLANK_PASSWORDS": "true", "USER_AS_PASS": "true", "USER_FILE": self.username, "PASS_FILE": self.plist}},]
            self.cmds = [{"name": self.proto+"_brute_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules_brute), "shell": True, "chain": False}]
