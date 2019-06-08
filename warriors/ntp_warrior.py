# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#apt-get install rpcbind
#You can check this module with irked.htb (10.10.10.117)

class Ntp_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": "ntp_nmap", "cmd": 'nmap -n -sV --script "ntp* and (discovery or vuln) and not (dos or brute)" -p ' + self.port + " " + self.host, "shell": False, "chain": False},
            {"name": "ntpq_readvar", "cmd": 'ntpq -c readvar ' + self.host, "shell": False, "chain": False},
            {"name": "ntpq_monlist", "cmd": 'ntpq -c monlist ' + self.host, "shell": False, "chain": False},
            {"name": "ntpq_peers", "cmd": 'ntpq -c peers ' + self.host, "shell": False, "chain": False},
            {"name": "ntpq_listpeers", "cmd": 'ntpq -c listpeers ' + self.host, "shell": False, "chain": False},
            {"name": "ntpq_ntpversion", "cmd": 'ntpq -c ntpversion ' + self.host, "shell": False, "chain": False},
            {"name": "ntpq_sysinfo", "cmd": 'ntpq -c sysinfo ' + self.host, "shell": False, "chain": False},
        ]
