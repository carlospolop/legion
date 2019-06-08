# -*- coding: utf-8 -*-

from warriors.warrior import Warrior


class Checkpoint_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        msfmodules = [{"path": "auxiliary/gather/checkpoint_hostname", "toset": {"RHOSTS": self.host, "RPORT": self.port}}]
        self.cmds = [{"name": self.proto+"_msf_"+self.port, "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False}]
