# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

#You can test this module against sizzle.htb (10.10.10.103)

class Dns_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        # TODO: ADD DNSsec attacks and other IPv6 attacks

        self.cmds = [
            {"name": "dnsrecon_127.0.0.0_24", "cmd": 'dnsrecon -r 127.0.0.0/24 -n ' + self.host, "shell": False, "chain": False},
            {"name": "dnsrecon_127.0.1.0_24", "cmd": 'dnsrecon -r 127.0.1.0/24 -n ' + self.host, "shell": False, "chain": False},
            {"name": "dns_nmap_tcp_"+self.port, "cmd": 'nmap -n -sV --script "(*dns* and (default or (discovery and safe))) or dns-random-txid or dns-random-srcport" -p ' + self.port + ' ' + self.host, "shell": True, "chain": False} ,
            {"name": "dns_nmap_udp_" + self.port,"cmd": 'nmap -n -sV -sU --script "(*dns* and (default or (discovery and safe))) or dns-random-txid or dns-random-srcport" -p ' + self.port + ' ' + self.host,"shell": True, "chain": False},

        ]

        if self.ip != "":
            self.cmds.append({"name": "dig_NS_"+self.port, "cmd": 'dig -x ' + self.ip + ' @' + self.host, "shell": False, "chain": False})
            self.cmds.append({"name": "dnsrecon_"+self.ip+"_24", "cmd": 'dnsrecon -r '+self.ip+'/24 -n ' + self.host, "shell": False, "chain": False})

        if self.ipv6 != "":
            self.cmds.append({"name": "dig_NS", "cmd": 'dig -x ' + self.ipv6 + ' @' + self.host, "shell": False, "chain": False})

        if self.intensity >= "2":
            msfmodules_vuln = [{"path": "auxiliary/scanner/dns/dns_amp", "toset": {"RPORT": self.port, "RHOSTS": self.host}}]
            self.cmds.append({"name": "dns_msf_vuln_"+self.port, "cmd": self.create_msf_cmd(msfmodules_vuln), "shell": True, "chain": False})

        if self.domain != "":
            self.cmds.append({"name": "dig", "cmd": self.dig_cmds(["axfr", "ANY", "A", "AAAA", "TXT", "MX", "NS", "SOA"]), "shell": True, "chain": False})
            self.cmds.append({"name": "dnsrecon_domain", "cmd": 'dnsrecon -d '+ self.domain + ' -a -n '+self.host, "shell": False, "chain": False})
            msfmodules = [{"path": "auxiliary/gather/enum_dns", "toset": {"DOMAIN": self.domain, "NS": self.host}}]
            self.cmds.append({"name": "DNS_msf", "cmd": self.create_msf_cmd(msfmodules), "shell": True, "chain": False})

            if self.intensity == "3":
                self.wordlist = self.plist if self.plist != "" else self.wordlists_path+'/subdomains.txt'
                self.cmds = [{"name": "dnsrecon_brute", "cmd": 'dnsrecon -D ' + self.wordlist + ' -d ' + self.domain + ' -n ' + self.host, "shell": False, "chain": False}]


    def dig_cmds(self, cmds):
        final_cmd = ""
        for cmd in cmds:
            final_cmd += "dig "+cmd+" @"+self.host+" "+self.domain+";"
        return final_cmd
