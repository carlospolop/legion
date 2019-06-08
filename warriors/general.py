# -*- coding: utf-8 -*-

import os

from time import sleep
from termcolor import colored
from threading import Thread

from warriors.warrior import Warrior
from lib.main import main_run
from lib.main import valid_protos
from lib.protocols import general_protocol

#The workdir of general is /home/username/.legion/host//

class General(Warrior):
    def __init__(self, parser, host, port, workdir, proto, intensity, username, ulist, password, plist, notuse, engine, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        self.parser = parser
        Warrior.__init__(self, host, port,  workdir, general_protocol, intensity, username, ulist, password, plist, notuse, engine, path, reexec, ipv6, domain, interactive, verbose, executed, exec)
        self.engine, self.ipv6 = "", ""
        self.protohelp = False
        self.checked = []
        self.stop = False
        self.ws = []
        self.myexecuted = []

    def run_proto(self, line, proto, port):
        if proto+port in self.myexecuted:
            return
        else:
            self.myexecuted.append(proto+port)
        for w in self.ws:
            self.executed.append(w.get_executed())
        if line:
            print()
            print(colored("Found " + str(port) + " opened for " + proto + ", sending warriors...: ", "blue", attrs=['bold'])+colored(line, "yellow", attrs=['bold']))

        warrior = main_run(self.parser, proto, self.host, self.workdir+"/../../", port, self.intensity, self.username, self.ulist, self.plist, self.protohelp,
                 self.notuse, self.engine, self.path, self.password, self.ipv6, self.domain, self.interactive, self.verbose, self.reexec, self.executed, self.exec)
        self.ws.append(warrior)
        thread = Thread(target=warrior.run)
        thread.start()
        sleep(3)

    def get_warriors(self):
        return self.ws

    def run(self):
        self.run_proto("", "scanner", "1337")

        while not self.stop:
            for root, dirs, files in os.walk(self.workdir+"/../scanner/"):
                for file in files:
                    with open(os.path.join(root, file), 'r') as f:
                        cont = f.readlines()

                    self.check_cont(cont, file)
            sleep(2)

    def check_cont(self, cont, file):
        if "nmap" in file:
            for line in cont:
                if line[0] in '1234567890':  # If 1st number, then port
                    port = line.split("/")[0]
                    if "tcp" in line and "open" in line:
                        for p in valid_protos:
                            if "tcp" in valid_protos[p].defproto:
                                if port in valid_protos[p].defports or (not (valid_protos[p].only_ports) and any([n in line for n in valid_protos[p].nmap])):
                                    self.run_proto(line, valid_protos[p].name, port)
                                    break

                    elif "udp" in line and "open" in line and not "filtered" in line:
                        for p in valid_protos:
                            if "udp" in valid_protos[p].defproto:
                                if port in valid_protos[p].defports or (not (valid_protos[p].only_ports) and any([n in line for n in valid_protos[p].nmap])):
                                    self.run_proto(line, valid_protos[p].name, port)
                                    break

        if "udp-proto-scanner" in file:
            for line in cont:
                if line.split(" ")[0] == "Received":
                    if "DNSVersionBindReq" in line:
                        self.run_proto(line, "dns", "53")
                    elif "snmp-public" in line:
                        self.run_proto(line, "snmp", "161")
                    elif "ike" in line:
                        self.run_proto(line, "ike", "500")


    def stop_general(self):
        self.stop = True
