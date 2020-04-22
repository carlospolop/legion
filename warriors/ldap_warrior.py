# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#You can test this module against sizzle.htb (10.10.10.103) and ypuffy (10.10.10.107)

class Ldap_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": "ldap_nmap_"+self.port, "cmd": 'nmap -n -sV --script "ldap* and not brute" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},
        ]

        if self.intensity >= "2":
            if domain != "" and path != "":
                self.cmds.append({"name": "ldapsearch", "cmd": "ldapsearch -x -h " +self.host+ " -D '" +self.domain+ "\\" +self.username+ "' -w '" +self.password+ "' -b 'DC=" +self.domain+ ",DC=" +self.path+ "'", "shell": True, "chain": False})
            if username != "" and password != "" and domain != "":
                self.cmds.append({"name": "ldapdomaindump", "cmd": "ldapdomaindump --no-json --no-grep --authtype SIMPLE -o "+self.workdir+" -r " +self.host+ " -u '" + self.domain + "\\" + self.username + "' -p '" + self.password+"' && echo 'To see the HTML output go to: "+self.workdir+"'", "shell": True, "chain": False})

        #The script ldap-brute lock accounts very fast, is better to not use it
        #if self.intensity:
        #    self.cmds = [
        #        {"name": "nmap_ldap", "cmd": 'nmap -sV --script "ldap*" -p ' + self.port + ' ' + self.host, "shell": False,
        #         "chain": False},
        #    ]
