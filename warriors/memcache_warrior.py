# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Memcache_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds = [
            {"name": self.proto + "_nmap_"+self.port, "cmd": 'nmap -n -sV --script memcached-info -p ' + self.port + ' ' + self.host, "shell": True, "chain": False},
            {"name": self.proto + "_stats_"+self.port, "cmd": 'echo -e "stats\n" | nc -vn ' + self.host + ' ' + self.port, "shell": True, "chain": False},
        ]
