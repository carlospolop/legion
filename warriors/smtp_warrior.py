# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Smtp_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n --script "smtp-open-relay or (default and *smtp*)" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},

        ]

        if self.proto == "smtp":
            self.cmds.append({"name": self.proto+"_version_"+self.port, "cmd": 'nc -w 20 -q 1 -vn ' + self.host + ' ' + self.port + ' </dev/null', "shell": True, "chain": False})
        else:
            self.cmds.append({"name": self.proto+"_version_"+self.port, "cmd": 'echo QUIT | openssl s_client -starttls smtp -crlf -connect '+self.host+':'+self.port, "shell": True, "chain": False})


        msfmodules = [{"path": "auxiliary/scanner/smtp/smtp_version", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                      {"path": "auxiliary/scanner/smtp/smtp_ntlm_domain", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                      {"path": "auxiliary/scanner/smtp/smtp_relay", "toset": {"RHOSTS": self.host, "RPORT": self.port}},
                      ]
        self.cmds.append({"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.intensity == 2:
            self.cmds.append({"name": self.proto+"_nmap_vuln_"+self.port, "cmd": 'nmap --script smtp-vuln-cve2011-1764,smtp-vuln-cve2011-1720,smtp-vuln-cve2010-4344  ' + self.host + ' ' + self.port, "shell": True, "chain": False})

        if self.intensity == "3":  # TODO: think about using other methods like RCT
            self.extra_info = "By default VRFY method is used, if you want to use other (EXPN or RCPT) set it in 'path' variable."
            self.extra_info += "\nYou can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            self.path = "VRFY" if self.path.upper() not in ["EXPN", "RCPT"] else self.path.upper()
            if username != "":
                self.cmds = [{"name": self.proto+"_brute", "cmd": 'smtp-user-enum -M '+self.path+' -u ' + self.username + ' -p ' + self.port + ' -t ' + self.host, "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": self.proto+"_brute", "cmd": 'smtp-user-enum -M '+self.path+' -U ' + self.ulist + ' -p ' + self.port + ' -t ' + self.host, "shell": True, "chain": False}]


