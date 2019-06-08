#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, signal

from threading import Thread
from termcolor import colored
from cmd import Cmd
from time import sleep

from lib.main import main_run
from lib.main import valid_protos
from lib.main import print_error
from warriors.general import General


class LegionPrompt(Cmd):
    intro = """\
    
██╗     ███████╗ ██████╗ ██╗ ██████╗ ███╗   ██╗
██║     ██╔════╝██╔════╝ ██║██╔═══██╗████╗  ██║
██║     █████╗  ██║  ███╗██║██║   ██║██╔██╗ ██║
██║     ██╔══╝  ██║   ██║██║██║   ██║██║╚██╗██║
███████╗███████╗╚██████╔╝██║╚██████╔╝██║ ╚████║
╚══════╝╚══════╝ ╚═════╝ ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ v2.0"""+colored("\nI wanted to destroy everything beautiful I'd never have\n", 'red', attrs=['bold'])
    prompt = '('+colored("legion", 'blue', attrs=['bold'])+') > '

    def __init__(self, parser, proto, host, workdir, port, intensity, username, ulist, plist, notuse, extensions, path, password,
                 ipv6, domain, verbose):
        Cmd.__init__(self)
        self.all_values = {"proto": proto, "host": host, "workdir": workdir, "port": port, "intensity": intensity,
                           "username": username, "ulist": ulist, "plist": plist, "notuse": notuse, "extensions": extensions,
                           "path": path, "password": password, "ipv6": ipv6, "domain": domain, "verbose": verbose,
                           "reexec": False}

        self.priv_values = {"interactive": True, "protohelp": False, "executed": [], "exec": ""}
        self.parser = parser
        self.ws = []
        self.general = ""
        self.msgs = {}

    def emptyline(self):
        pass

    def do_exit(self, inp):
        '''exit the application'''
        print("Bye!")
        self.stop_procs()
        os.kill(os.getpid(), signal.SIGTERM)

    def do_quit(self, inp):
        '''exit the application'''
        print("Bye!")
        self.stop_procs()
        os.kill(os.getpid(), signal.SIGTERM)

    def do_stopall(self, inp):
        '''Stop ALL running processes'''
        self.stop_procs()

    def do_stop(self, procname):
        '''Stop a process given the name'''
        self.stop_p(procname)

    def do_protos(self, args):
        '''List the name of valid protocols'''
        c = 0
        for i, p in enumerate(valid_protos):
            clr = "green" if p not in ["scanner"] else "blue"
            myend = "\t\t" if len(p) < 8 else "\t"
            if c % 3 != 0:
                print(colored(p, clr, attrs=['bold']), end=myend)
            else:
                print("\n"+colored(p, clr, attrs=['bold']), end=myend)
            c += 1
        print()
        print(colored("There are a total of "+str(len(valid_protos))+" supported protocols", "yellow", attrs=['bold']))

    def do_set(self, args):
        '''Set variable value: set proto http'''
        if len(args.split(" ")) < 2:
            print_error("set <variable> <value>")
        else:
            variable = args.split(" ")[0].lower()
            value = args.split(" ")[1]
            if variable == "proto" and value.lower() not in valid_protos:
                print_error("Not valid protocol: "+value)
            elif variable.lower() in self.all_values:
                value = value if not value.lower() in ["true", "false"] else (True if value.lower() == "true" else False)
                self.all_values[variable] = value
                print(colored(variable.capitalize(), "blue", attrs=['bold']) + ": " + colored(str(value), "yellow", attrs=['bold']))
            else:
                print_error(variable + " is not valid")

    def do_unset(self, args):
        '''Set variable to null'''
        if len(args.split(" ")) < 1:
            print_error("unset <variable>")
        else:
            variable = args.split(" ")[0].lower()
            if variable.lower() in self.all_values:
                self.all_values[variable] = ""
                print(colored(variable.capitalize(), "blue", attrs=['bold']) + ": " + colored("Null", "magenta", attrs=['bold']))
            else:
                print_error(variable + " is not valid")

    def do_get(self, args):
        '''Get variable value: get proto'''
        variable = args.split(" ")[0].lower()
        if variable.lower() in self.all_values:
            print(variable + ": " + str(self.all_values[variable]))
        else:
            print_error(variable + " is not valid")

    def do_options(self, _):
        '''Get all Parameters and their value'''
        for key, value in sorted(self.all_values.items()):
            if key == "proto":
                print(colored(str(key) + ": ", 'yellow', attrs=['bold']) + str(value))
            else:
                print(colored(str(key)+": ", 'cyan', attrs=['bold'])+str(value))

    def do_procs(self, _):
        '''Get information about running and run processes'''
        self.print_procs(self.ws)
        if self.general != "":
            print()
            print(colored("Warriors sent by the General:", "blue", attrs=['bold', 'underline']))
            self.print_procs(self.general.get_warriors())
        print("")

    def do_out(self, filename):
        '''Get the output of a executed tool: getout smbclient'''
        name = filename + ".out"
        for root, dirs, files in os.walk(self.all_values["workdir"]+"/"+self.all_values["host"]):
            if name in files:
                with open(os.path.join(root, name), 'r') as f:
                    print(f.read())
                    break

    def do_err(self, filename):
        '''Get the error of a executed tool: geterr smbclient'''
        name = filename + ".err"
        for root, dirs, files in os.walk(self.all_values["workdir"]):
            if name in files:
                with open(os.path.join(root, name), 'r') as f:
                    print(f.read())
                    break
    
    def do_info(self, _):
        '''Get info of the selected protocol'''
        self.priv_values["protohelp"] = True
        self.initW()
        self.priv_values["protohelp"] = False

    def do_run(self, _):
        '''Execute the confiured protocol attack'''
        self.priv_values["protohelp"] = False
        self.update_executed()
        warrior = self.initW()

        if warrior != -1:  # If -1, then something went wrong creating the warrior
            self.ws.append(warrior)
            thread = Thread(target=warrior.run)
            thread.start()
        else:
            print_error("Something went wrong, nothing is going to be executed")

    def do_exec(self, args):
        '''Execute the indicated cmd'''
        if len(args.split(" ")) < 1:
            print_error("exec <CMDname>")
        cmd = args.split(" ")[0].lower()
        self.priv_values["exec"] = cmd
        warrior = self.initW()
        self.priv_values["exec"] = ""

        if warrior != -1:  # If -1, then something went wrong creating the warrior
            self.ws.append(warrior)
            thread = Thread(target=warrior.run)
            thread.start()
        else:
            print_error("Something went wrong, nothing is going to be executed")


    def do_startGeneral(self, _):
        '''Star a General that will help. Automatize the scan and launch of scripts depending on the discovered services. Only one at the same time is allowed.'''
        if self.general == "":
            print(colored("Starting General", "blue", attrs=['bold']))
            self.general = General(self.parser, self.all_values["host"], "0", self.all_values["workdir"], "/", self.all_values["intensity"],
                        self.all_values["username"], self.all_values["ulist"], self.all_values["password"], self.all_values["plist"],
                        self.all_values["notuse"], self.all_values["extensions"], self.all_values["path"], self.all_values["reexec"],
                        self.all_values["ipv6"], self.all_values["domain"], self.priv_values["interactive"],
                        self.all_values["verbose"], self.priv_values["executed"], self.priv_values["exec"])

            thread = Thread(target=self.general.run)
            thread.start()
        else:
            print(colored("general is already running... You can stop it with stopGeneral",'blue'))

    def do_stopGeneral(self, _):
        '''Stop the general'''
        print(colored("Stopping General...", 'blue', attrs=['bold']))
        self.general.stop_general()
        self.general = ""

    def initW(self):
        '''Initialize the current Warrior'''
        return main_run(self.parser, self.all_values["proto"], self.all_values["host"],
                 self.all_values["workdir"], self.all_values["port"], self.all_values["intensity"],
                 self.all_values["username"], self.all_values["ulist"],
                 self.all_values["plist"], self.priv_values["protohelp"], self.all_values["notuse"],
                 self.all_values["extensions"], self.all_values["path"], self.all_values["password"],
                 self.all_values["ipv6"], self.all_values["domain"], self.priv_values["interactive"],
                 self.all_values["verbose"], self.all_values["reexec"], self.priv_values["executed"],
                 self.priv_values["exec"])

    def print_procs(self, ws):
        last = ""
        ws = sorted(ws, key=lambda x: x.get_proto())
        for w in ws:
            if type(w) is int:
                print_error("An INT was found as a WARRIOR, TAKE A LOOK!")
                continue
            if last != w.get_proto():
                print()
                print(colored(w.get_proto(), 'blue', attrs=['reverse', 'bold']))
            last = w.get_proto()
            procs, ch = w.get_procs_info()
            procs = sorted(procs, key=lambda x: x["name"])
            for p in procs:
                if p["proc"].is_alive():
                    print(colored(p["name"] + ": ", 'yellow', attrs=['blink', 'bold']) + p["cmd"])
                else:
                    print(colored(p["name"] + ": ", 'green', attrs=['bold']) + p["cmd"])
            if ch:
                print(colored("Command require sequencial object, waiting for execute next commnad...", 'red', attrs=['bold']))

    def get_pids(self):
        for w in self.ws:
            self.msgs = {**self.msgs, **w.get_all_queue()}
        if self.general != "":
            for w in self.general.get_warriors():
                self.msgs = {**self.msgs, **w.get_all_queue()}

    def stop_p(self, param_name):
        self.get_pids()
        self.kill_pbyname(param_name)


    def stop_procs(self):
        self.proc_stop_procs(self.ws)
        if self.general != "":
            self.proc_stop_procs(self.general.get_warriors())

    def proc_stop_procs(self, ws):
        rep = True
        while rep:
            rep = False
            self.get_pids()
            for w in ws:
                procs, ch = w.get_procs_info()
                for p in procs:
                    if p["proc"].is_alive():
                        self.kill_pbyname(p["name"])
                        rep = True
                        sleep(0.5)

    def kill_pbyname(self, pname):
        if pname in self.msgs:
            os.kill(int(self.msgs[pname]), signal.SIGKILL)
            print(colored("Terminated: ", 'green', attrs=['bold']) + pname + "("+str(self.msgs[pname])+")")
        else:
            print(colored("Not found: ", 'red', attrs=['bold']) + pname)

    def update_executed(self):
        for w in self.ws:
            self.priv_values["executed"].append(w.get_executed())
        if self.general != "":
            for w in self.general.get_warriors():
                self.priv_values["executed"].append(w.get_executed())
