# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#You can test this module against sizzle.htb (10.10.10.103)
#Soft link to samrdump.py

class Smb_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": "enum4linux", "cmd": 'enum4linux -a -u "'+self.username+'" -p "'+self.password+'" '+self.host, "shell": True, "chain": False},
            {"name": "smb_nmap", "cmd": 'nmap -n -sV --script "(safe and smb*) or smb-enum-*" -p 135,139,445 ' + self.host, "shell": True, "chain": False},
            {"name": "smbmap_"+self.port, "cmd": 'smbmap -u "'+self.username+'" -p "'+self.password+'" -H '+self.host+" -P "+self.port, "shell": True, "chain": False},
            {"name": "smbclient", "cmd": "smbclient -U '"+self.username+"%"+self.password+"' -L //" + self.host, "shell": False, "chain": False},
            {"name": "nbtscan", "cmd": 'nbtscan ' + self.host, "shell": False, "chain": False},
            {"name": "smb_samrdump_"+self.port, "cmd": 'python $(which samrdump.py) -port ' + self.port + ' ' + self.host, "shell": False, "chain": False},
        ]

        msfmodules = [
            {"path": "auxiliary/scanner/smb/smb_version", "toset": {"RHOSTS": self.host}},
        ]
        self.cmds.append({"name": self.proto + "_msf", "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if username == "" or ("<" == username[0] and ">" == username[-1]):
            self.cmds.append({"name": "smbmap_guest_"+self.port, "cmd": 'smbmap -u "guest" -p "" -H '+self.host+" -P "+self.port, "shell": True, "chain": False})
            self.cmds.append({"name": "smbclient_guest", "cmd": "smbclient -U 'guest%' -L //" + self.host, "shell": True, "chain": False})
            self.cmds.append({"name": "enum4linux_guest", "cmd": 'enum4linux -a -u "guest" -p "" '+self.host, "shell": True, "chain": False})
