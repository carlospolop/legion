# -*- coding: utf-8 -*-

import sys, os, socket, re

from termcolor import colored
from subprocess import Popen
from multiprocessing import Process, Queue
from time import sleep


def print_error(msg):
    print(colored("[-] Error: "+msg, 'red', attrs=['bold']))

class Warrior:
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec):
        self.host = host
        self.port = port if port == "<PORT>" or int(port) > 0 < 65536 else protocol.defports[0]
        self.proto = protocol.name
        self.workdir = workdir + "/" + self.host + "/" + self.proto + "/" +self.port
        self.intensity = intensity
        self.username = username
        self.ulist = ulist
        self.password = password
        self.plist = plist
        self.notuse = notuse if type(notuse) is list else notuse.split(",")
        self.interactive = interactive
        self.verbose = verbose
        self.extensions = extensions
        self.path = path
        self.reexec = reexec
        self.ipv6 = ipv6
        self.domain = domain
        self.exec = exec

        self.q = Queue()                                        # Queue used to send the PID of the processes
        self.cmds = []                                          # CMDs that are going to be executed
        self.demand_cmds = []                                   # List of other possible CMDs to execute
        self.processes = []                                     # List of running/run processed
        self.executed = executed                                # List of name of processes executed
        self.proto_info = protocol.info                         # Basic protocol information
        self.proto_url = protocol.url                           # URL with more info about the protocol
        self.extra_info = ""                                    # This should be overwritten inside the warrior, if needed
        self.defport_info = {"ports": protocol.defports, "tcp": "tcp" in protocol.defproto, "udp": "udp" in protocol.defproto}  # Info about the default ports used
        self.proto_host = self.proto+"://"+self.host            # http://127.0.0.1
        self.host_port = self.host+":"+self.port                # Ex: 127.0.0.1:8080
        self.proto_host_port = self.proto_host+":"+self.port    # Ex: http://127.0.0.1:8080
        self.proto_host_port_path = self.proto_host + ":" + self.port + self.path  # Ex: http://127.0.0.1:8080/some/path.php
        self.victim_file = self.workdir+"/"+"victim"            # File where the host is written
        self.isChained = False                                  # Process needs to wait to finish before executing next
        self.ip = self.host if re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", self.host) else ""  # If host is an IP fill this field
        self.wordlists_path = os.path.dirname(os.path.realpath(__file__)) + '/../wordlists/'
        self.git_path = os.path.dirname(os.path.realpath(__file__)) + '/../git/'

        self.ulist = ulist if len(ulist) > 0 else self.wordlists_path + '/users.txt'
        self.plist = plist if len(plist) > 0 else self.wordlists_path + '/passwords.txt'

        # If host is a domain
        if re.match("^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$", self.host):
            self.ip = socket.gethostbyname(self.host)                       # If host is a domain, get the IP
            self.domain = self.host if self.domain == "" else self.domain   # If host is a domain, fill this field

        self.write_host()

    def execute(self, q, cmd, name, shell=False):
        cmdl = cmd
        if not shell:
            cmd = cmd.split(" ")
        with open(self.workdir+"/"+name+".out", "wb") as out, open(self.workdir+"/"+name+".err", "wb") as err:
            try:
                pw = Popen(cmd, stdout=out, stderr=err, shell=shell)
                print(colored("Executing ",'yellow', attrs=['bold']) + colored(name, 'cyan', attrs=['bold']) + colored(" with PID: ", 'yellow', attrs=['bold']) + colored(str(pw.pid), 'cyan', attrs=['bold']) + colored(" Command: ", 'yellow', attrs=['bold'])+ cmdl)
                q.put(name+","+str(pw.pid))
                pw.communicate()
            except Exception as e:
                print_error("Something has happened with "+name+" (Exception: "+str(e)+")")
        if self.interactive:
            print(colored(name, 'green', attrs=['bold']))
            if self.verbose:
                self.getout(name)

    def get_all_queue(self):
        '''Obtiene la relacion  "nombre",pid  de los mensajes de la cola'''
        msgs = []
        fm = {}
        while not self.q.empty():
            msgs.append(self.q.get())

        for msg in msgs:
            msgsplit = msg.split(",")
            if len(msgsplit) > 1:
                fm[msgsplit[0]] = msgsplit[1]
        return fm

    def get_executed(self):
        return self.executed

    def exec_proc(self, cmd):
        CY = '\033[33m'
        NC = '\033[0m'
        p = { "name": cmd["name"], "cmd": cmd["cmd"] }
        p["proc"] = Process(target=self.execute, args=(self.q, cmd["cmd"], cmd["name"], cmd["shell"]))
        self.processes.append(p)
        self.processes[-1]["proc"].start()
        if cmd["chain"]:  # If chain, wait it to finish
            self.isChained = True
            if not self.interactive:
                sys.stdout.write('\r'+CY+"[I] Waiting..."+NC)
            self.processes[-1]["proc"].join()
            if not self.interactive:
                sys.stdout.flush()
            self.isChained = False

    def get_procs_info(self):
        return (self.processes, self.isChained)

    def get_proto(self):
        return self.proto

    def print_help(self):
        l4_proto = "tcp,udp" if self.defport_info["tcp"] and self.defport_info["udp"] else ("tcp" if self.defport_info["tcp"] else ("udp" if self.defport_info["udp"] else ""))
        print(colored("Protocol Resume", "blue", attrs=['bold', 'underline']))
        print(colored(self.proto_info, "green", attrs=['bold']))
        if self.defport_info["ports"]:
            print(colored("Default(s) port: ", "blue", attrs=['bold']) + ", ".join(self.defport_info["ports"]) + "("+colored(l4_proto, "blue")+")" )
        if self.proto_url:
            print(colored("URL with more information: ", "blue", attrs=['bold']) + colored(self.proto_url,'cyan', attrs=['bold']))
        if self.extra_info:
            print(colored(self.extra_info, "magenta", attrs=['bold']))
        print()
        print("For "+colored(self.proto.upper(), 'cyan', attrs=['bold'])+" will be executed:")
        for cmd in self.cmds:
            if all([(tool not in cmd["cmd"]) if len(tool) > 1 else True for tool in self.notuse]):  # Check for notuse
                print(colored(cmd["name"]+":", 'blue', attrs=['bold']), colored(cmd["cmd"], 'yellow', attrs=['bold']))
        print()
        if self.demand_cmds:
            if all([(tool not in cmd["cmd"]) if len(tool) > 1 else True for tool in self.notuse]):  # Check for notuse
                print("For " + colored(self.proto.upper(), 'cyan', attrs=['bold']) + " on demand cmds could be executed:")
                for cmd in self.demand_cmds:
                    print(colored(cmd["name"] + ":", 'blue', attrs=['bold']), colored(cmd["cmd"], 'yellow', attrs=['bold']))

    def write_host(self):
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
        with open(self.victim_file,'w') as f:
            f.write(self.host)

    def run(self):
        CG = '\033[92m'
        NC = '\033[0m'
        if self.exec != "":
            for cmd in self.demand_cmds + self.cmds:
                if self.exec in cmd["name"]:
                    self.executed.append(cmd)
                    self.exec_proc(cmd)
                    sleep(0.15)
        else:
            for cmd in self.cmds:
                if all([(tool not in cmd["cmd"]) if len(tool)>1 else True for tool in self.notuse]) and (cmd not in self.executed or self.reexec):  # Check for notuse
                    self.executed.append(cmd)
                    self.exec_proc(cmd)
                    sleep(0.15)
        if not self.interactive:
            while any(p["proc"].is_alive() for p in self.processes):
                sleep(1)
                sys.stdout.flush()
                to_write = "\rProcessing "+", ".join([p["name"] if p["proc"].is_alive() else CG+p["name"]+NC for p in self.processes])+"\t\t\tCompleted: {0:03}%".format(int(len([p for p in self.processes if not p["proc"].is_alive()])*100/len(self.processes)))
                sys.stdout.write(to_write)
            sys.stdout.flush()

    def getout(self, filename):
        '''Get the output of a executed tool: getout smbclient'''
        name = filename + ".out"
        for root, dirs, files in os.walk(self.workdir):
            if name in files:
                with open(os.path.join(root, name), 'r') as f:
                    print(f.read())
                    break

    def create_msf_cmd(self, params):
        cmd = "msfconsole -q -x '"
        for param in params:
            cmd += "use " + param["path"] + ";"
            for key in param["toset"]:
                cmd += "set "+key+" "+param["toset"][key]+";"
            cmd += "run;"
        cmd += "exit'"
        return cmd
