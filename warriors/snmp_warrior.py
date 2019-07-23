# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#Revisado
#apt-get install snmp-mibs-downloader
# in /etc/snmp/snmp.conf comment the line "mibs :"

#You can test this module against condeal.htb (10.10.10.116)

class Snmp_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)
        self.community = self.password if len(self.password)>0 else "public"
        self.plist = plist if plist != "" else self.wordlists_path+'/snmp_default_pass.txt'

        self.extra_info += "\nBy default the community string used is 'public'. If you want to use other, set it in the 'password' variable."

        self.cmds = [
            {"name": "snmpwalkv1", "cmd": 'snmpwalk -v 1 -c ' + self.community + ' ' + self.host, "shell": False, "chain": False},
            {"name": "snmpwalkv2c", "cmd": 'snmpwalk -v 2c -c ' + self.community + ' ' + self.host, "shell": False, "chain": False},
            {"name": "snmp_nmap_"+self.port, "cmd": 'nmap -n -sV --script "*snmp* and not brute and not dos" -p ' +self.port + " " + self.host, "shell": True, "chain": False},

        ]
        
        msfmodules = [{"path": "auxiliary/scanner/smb/smb2", "toset": {"RHOSTS": self.host, "RPORT": self.port}}]

        self.cmds.append({"name": "smb_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

        if self.ip != "":
            self.cmds.append({"name": "snmp_check1_"+self.port, "cmd": 'snmp-check -p '+ self.port + ' -c ' + self.community + ' ' + self.ip, "shell": False, "chain": False})
            self.cmds.append({"name": "snmp_check2c_"+self.port, "cmd": 'snmp-check -v 2c -p ' + self.port + ' -c ' + self.community + ' ' + self.ip, "shell": False, "chain": False})

        if self.intensity == "3":
            self.cmds = [{"name": "snmp_brute_hydra_"+self.port, "cmd": 'hydra -f -P ' + self.plist + ' -s ' +self.port + ' ' + self.host + ' snmp', "shell": False, "chain": False}]

