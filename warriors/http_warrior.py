# -*- coding: utf-8 -*-

from warriors.warrior import Warrior

class Http_warrior (Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        Warrior.__init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec)

        self.cmds=[
            {"name": self.proto+"_nikto_"+self.port, "cmd": 'echo n | nikto -nointeractive -maxtime 45m -timeout 60 -host '+self.proto_host_port_path+' -Plugins "paths;outdated;report_sqlg;auth;content_search;report_text;fileops;parked;shellshock;report_html;cgi;headers;report_nbe;favicon;cookies;robots;report_xml;report_csv;ms10_070;msgs;drupal;apache_expect_xss;siebel;put_del_test;apacheusers;dictionary;embedded;ssl;clientaccesspolicy;httpoptions;subdomain;negotiate;sitefiles;mutiple_index;strutshock;dishwasher;paths;docker_registry;origin_reflection;dir_traversal;multiple_index"', "shell": True, "chain": False},
            {"name": self.proto+"_whatweb_"+self.port, "cmd": "whatweb -a 3 "+self.proto_host_port_path, "shell": False, "chain": False},
            {"name": self.proto + "_robots_"+self.port, "cmd": 'curl ' + self.proto_host_port + '/robots.txt -L -k --user-agent "Googlebot/2.1 (+http://www.google.com/bot.html)" --connect-timeout 30 --max-time 180', "shell": True, "chain": False},
            {"name": self.proto+"_nmap_"+self.port, "cmd": 'nmap -n -sV --script "(http* and not (dos or brute) and not http-xssed)" -p '+self.port+' '+self.host, "shell": True, "chain": False},
            {"name": self.proto+"_wafw00f_"+self.port, "cmd": 'wafw00f '+self.proto_host_port_path, "shell": False, "chain": False},
            {"name": self.proto+"_fast_dirsearch_"+self.port, "cmd": "dirsearch -F -r -u " + self.proto_host_port_path + " -e " + self.extensions, "shell": False,"chain": False},
            {"name": self.proto+"_dirhunt_"+self.port, "cmd": "dirhunt "+self.proto_host_port_path, "shell": False, "chain": False},
            #{"name": "gobuster", "cmd": "gobuster -k -fw -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u "+self.proto_host_port_path+" -x html,txt,"+self.extensions, "shell": False, "chain": False},
            #{"name":"dirb","cmd": "dirb -S " + self.proto_host_port_path + " -X ." + self.extensions.replace(",",",."), "shell": False, "chain": False}, #Dirb needs the extension with a point. The flag '-f' in dirsearch makes it behave like dirb (force ext and "/")
            {"name": self.proto+"_cmsmap_"+self.port, "cmd": 'echo "y" | cmsmap -s '+self.proto_host_port_path, "shell": True, "chain": False},
            {"name": self.proto + "_curl_put_"+self.port, "cmd": 'curl -v -X PUT -d "Hey! I am a PUT" ' + self.proto_host_port_path + "/legion.txt", "shell": True, "chain": False},
            {"name": self.proto + "_gobuster_vhosts_"+self.port, "cmd": 'gobuster vhost -u "' + self.proto_host_port + '" -t 50 -w "' + self.wordlists_path+'/subdomains-top1million-110000.txt"', "shell": True, "chain": False},

        ]

        #if self.domain and self.ip:
        #    self.cmds.append({"name": self.proto+"_vhost-brute", "cmd": "vhost-brute.php --domain "+self.domain+" --ip "+self.ip+" --wordlist "+self.wordlists_path+'/subdomains.txt' + (" --ssl" if self.proto == "https" else ""), "shell": False, "chain": False})

        if self.proto == "https":
            self.cmds.append({"name": "https_sslscan_"+self.port, "cmd": "sslscan "+self.host_port, "shell": False, "chain": False})
            self.cmds.append({"name": "https_sslyze_"+self.port, "cmd": "sslyze --regular "+self.host_port, "shell": False, "chain": False})
            self.cmds.append({"name": "https_ssl_nmap_"+self.port, "cmd": 'nmap -sV --script "ssl-* and not brute and not dos" -p ' + self.port + " " +self.host, "shell": True, "chain": False})

        if self.intensity >= "2":
            self.cmds.append({"name": self.proto + "_medium_dirsearch_"+self.port, "cmd": "dirsearch -f -F -r -u " + self.proto_host_port_path + " -e " + self.extensions + " -w /usr/share/dirb/wordlists/common.txt", "shell": False, "chain": False})
            self.cmds.append({"name": self.proto + "_medium_dirsearch_raft_"+self.port, "cmd": "dirsearch -f -F -r -u " + self.proto_host_port_path + " -e " + self.extensions + ' -w ' + self.wordlists_path+'/raft-medium-words.txt', "shell": False, "chain": False})

        if self.intensity == "3":
            self.extra_info = "You can use the variable 'username' to brute force a single username or the variable ulist to bruteforce a list of usernames. The default 'path' is '/'."
            if username != "":
                self.cmds = [{"name": self.proto + "_brute_hydra_"+self.port, "cmd": "hydra -l "+self.username+" -P "+self.plist+" "+self.host+" "+self.proto+"-get -s "+self.port+" -f -e ns -m "+self.path, "shell": False, "chain": False}]
            else:
                self.cmds = [{"name": self.proto + "_brute_hydra_"+self.port, "cmd": "hydra -L "+self.ulist+" -P "+self.plist+" "+self.host+" "+self.proto+"-get -s "+self.port+" -f -e ns -m "+self.path, "shell": False, "chain": False}]

        dav_auth = "-auth "+self.username+":"+self.password+" " if (self.username and self.password) else ""
        self.demand_cmds=[
            {"name": self.proto + "_slow_dirsearch_"+self.port, "cmd": "dirsearch -f -F -u " + self.proto_host_port + " -e " + self.extensions + " -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt", "shell": False, "chain": False},
            {"name": self.proto + "_sqlmap_"+self.port, "cmd": "sqlmap -u "+self.proto_host_port_path+" --batch --crawl=3 --forms --random-agent --level 1 --risk 1 -f -a" , "shell": False, "chain": False},
            {"name": self.proto + "_davtestmove_"+self.port, "cmd": "davtest "+dav_auth+"-move -sendbd auto -url "+self.proto_host_port_path, "shell": False, "chain": False},
            {"name": self.proto + "_davtestnorm_"+self.port, "cmd": "davtest "+dav_auth+" -sendbd auto -url " + self.proto_host_port_path, "shell": False, "chain": False},
            {"name": self.proto + "_wpscan_"+self.port, "cmd": "wpscan --url "+self.proto_host_port_path+" --rua --no-update --enumerate ap", "shell": False, "chain": False},
            {"name": self.proto + "_cewl_"+self.port, "cmd": "cewl "+self.proto_host_port_path+" -m 6", "shell": False, "chain": False},
            {"name": self.proto + "_arjun_"+self.port, "cmd": "cd "+ self.git_path+"/arjun 2>/dev/null; ./arjun.py --get -u "+self.proto_host_port_path+"; "+
                                                            "./arjun.py --post -u "+self.proto_host_port_path+"; "+
                                                            "./arjun.py --json -u "+self.proto_host_port_path+"; cd - 2>/dev/null",
            "shell": True, "chain": False},
        ]
