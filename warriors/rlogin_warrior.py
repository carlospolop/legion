# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Rlogin_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames."
            if username != "":
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -l '+self.username+' -P '+self.plist+' -s '+self.port+' '+self.host+' rlogin', "shell": True, "chain": False}]
            else:
                self.cmds = [{"name": self.proto+"_brute_hydra_"+self.port, "cmd": 'hydra -f -e ns -L ' + self.ulist + ' -P ' + self.plist + ' -s ' + self.port + ' ' + self.host + ' rlogin',"shell": True, "chain": False}]

