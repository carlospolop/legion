#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse, sys, os

from lib.main import main_run
from lib.interact import LegionPrompt
from os.path import expanduser

# Execute: python3 legion.py <protocol> --host <IP> [--port <PORT>] [--workdir <PATH>] [-v] [-b] [-u <username] [-U usernamesList] [-P passwordsList] [--protohelp] [--notuse <Ex: nmap,gobuster,dirsearch>]  


def check_args(args=None):
    parser = argparse.ArgumentParser(description='Automatically analyze +45 protocols.')
    parser.add_argument('--proto', default='scanner',
                        help='Protocol to test (Default: "scanner")')
    parser.add_argument('--host', default="127.0.0.1",
                        help='Host to test (Default: 127.0.0.1)')
    parser.add_argument('--workdir', default=expanduser("~")+'/.legion/',
                        help='Working directory (Default: '+expanduser("~")+'/.legion/)')
    parser.add_argument('-p', '--port',  type=int, default=0,
                        help='Port where the protocol is listening (default one will be used if not set). Always default is used by: DNS, RCPinfo')
    parser.add_argument('-i', '--intensity', type=int,
                        default=2, help='1-Main checks, 2-Main and more vulns checks (default), 3-Only Service Bruteforce')
    parser.add_argument('-u', '--username',
                        default="", help='Username to use in bruteforce')
    parser.add_argument('-U', '--ulist', default="",
                        help='Usernames to use in bruteforce (Windows and Unix users list setted by default)')
    parser.add_argument('-k', '--password',
                        default="", help='Password to use(smb, community snmp, groupid IKE)')
    parser.add_argument('-P', '--plist', default="",
                        help='Passwords to use in bruteforce (passwords to brute, dnssubdomain brute, snmp communities brute setted by default to the protocols who need them)')
    parser.add_argument('--protohelp',  action="store_true",
                        default=False, help='Set to get help of selected protocol')
    parser.add_argument('--notuse', default="",
                        help='Comma separate string of name of tools that you dont want to be used')
    parser.add_argument('--extensions', default="html,txt,php,asp,aspx",
                        help='USED IN HTTP/s: Set valid extensions of the web server (Default: html,txt,php,asp,aspx)')
    parser.add_argument('--path', default="",
                        help='USED IN HTTP/s: Set the URL path like /path/to/file.php')
    parser.add_argument('--ipv6', default="",
                        help='USED IN HTTP/s: Used for reverse dns lookup with ipv6')
    parser.add_argument('--domain', default="",
                        help='If possible, set the domain name here and the VictimIP in --host')
    parser.add_argument('--execonly', default="",
                        help='Exec only this tool')
    parser.add_argument('-r', '--run', action="store_true", default=False,
                        help='Just run the analysis')
    parser.add_argument('-v', '--verbose', action="store_true", default=True,
                        help='Get output when the command finish (default: True)')

    args = parser.parse_args()
    return (parser, args.proto.lower(), args.host, args.workdir, str(args.port), str(args.intensity), args.username,
            args.ulist, args.plist, args.protohelp, args.notuse.split(","), args.extensions, args.path, args.password,
            args.ipv6, args.domain, args.execonly, args.run, args.verbose)


def main():
    parser, proto, host, workdir, port, intensity, username, ulist, plist, protohelp, notuse, extensions, path, password, ipv6, \
        domain, execonly, run, verbose = check_args(sys.argv[1:])

    interactive = not run

    if os.getuid() != 0:
        exit("Please, execute this script as root.")

    try:
        if not os.path.isdir(workdir):
            os.mkdir(workdir)
    except Exception as e:
        print("The workdir directory: '"+workdir+"' could not be created!\nExiting...")

    if not interactive:
        main_run(parser, proto, host, workdir, port, intensity, username, ulist, plist, protohelp, notuse, extensions, path,
                 password, ipv6, domain, interactive, verbose, False, [], execonly)

    else:
        LegionPrompt(parser, proto, host, workdir, port, intensity, username, ulist, plist, notuse, extensions, path, password,
                     ipv6, domain, verbose).cmdloop()


if __name__ == "__main__":
    main()
