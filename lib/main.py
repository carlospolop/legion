#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os, re

from termcolor import colored

from lib.protocols import valid_protos
from warriors.afp_warrior import Afp_warrior
from warriors.ajp_warrior import Ajp_warrior
from warriors.bacnet_warrior import Bacnet_warrior
from warriors.cassandra_warrior import Cassandra_warrior
from warriors.checkpoint_warrior import Checkpoint_warrior
from warriors.couchdb_warrior import Couchdb_warrior
from warriors.dns_warrior import Dns_warrior
from warriors.enip_warrior import Enip_warrior
from warriors.finger_warrior import Finger_warrior
from warriors.ftp_warrior import Ftp_warrior
from warriors.scanner_warrior import Scanner_warrior
from warriors.http_warrior import Http_warrior
from warriors.ike_warrior import Ike_warrior
from warriors.imap_warrior import Imap_warrior
from warriors.irc_warrior import Irc_warrior
from warriors.iscsi_warrior import Iscsi_warrior
from warriors.ldap_warrior import Ldap_warrior
from warriors.memcache_warrior import Memcache_warrior
from warriors.modbus_warrior import Modbus_warrior
from warriors.mongodb_warrior import Mongodb_warrior
from warriors.mssql_warrior import Mssql_warrior
from warriors.mysql_warrior import Mysql_warrior
from warriors.ndmp_warrior import Ndmp_warrior
from warriors.nfs_warrior import Nfs_warrior
from warriors.ntp_warrior import Ntp_warrior
from warriors.oracle_warrior import Oracle_warrior
from warriors.pgsql_warrior import Pgsql_warrior
from warriors.pjl_warrior import Pjl_warrior
from warriors.pop_warrior import Pop_warrior
from warriors.portmapper_warrior import Portmapper_warrior
from warriors.rdp_warrior import Rdp_warrior
from warriors.redis_warrior import Redis_warrior
from warriors.rexec_warrior import Rexec_warrior
from warriors.rlogin_warrior import Rlogin_warrior
from warriors.jrmi_warrior import Jrmi_warrior
from warriors.rsh_warrior import Rsh_warrior
from warriors.rsync_warrior import Rsync_warrior
from warriors.rtsp_warrior import Rtsp_warrior
from warriors.saprouter_warrior import Saprouter_warrior
from warriors.smb_warrior import Smb_warrior
from warriors.smtp_warrior import Smtp_warrior
from warriors.snmp_warrior import Snmp_warrior
from warriors.ssh_warrior import Ssh_warrior
from warriors.telnet_warrior import Telnet_warrior
from warriors.vnc_warrior import Vnc_warrior
from warriors.wrpc_warrior import Wrpc_warrior
from warriors.x11_warrior import X11_warrior


def print_error(msg):
    print(colored("[-] Error: "+msg, 'red', attrs=['bold']))

def main_run(parser, proto, host, workdir, port, intensity, username, ulist, plist, protohelp, notuse, extensions, path, password,
             ipv6, domain, interactive, verbose, reexec, executed, exec):

    if not proto in valid_protos:
        if not interactive:
            parser.print_help(sys.stderr)
            sys.exit(1)
        else:
            print_error("Protocol '"+proto+"' is not valid")
            return -1

    if not os.path.isdir(workdir) or not os.access(workdir, os.W_OK):
        if not interactive:
            parser.print_help(sys.stderr)
            print_error("Not valid directory or not writable: " + workdir)
            sys.exit(2)
        else:
            print_error("Not valid directory or not writable: " + workdir)
            return -1

    if not protohelp and not host:
        if not interactive:
            parser.print_help(sys.stderr)
            print_error("A host is needed")
            sys.exit(3)
        else:
            print_error("Please, set a host")
            return -1

    # Heck domain name, ip and ip range if scanner
    if not re.match("^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$", host) and \
        not re.match(
            "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",
            host) and \
        not (proto == "scanner" and re.match(
            "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])/\d{1,2}$",
            host)):
                
        if not interactive:
            parser.print_help(sys.stderr)
            print_error("The provided host is not an IP nor a valid Domain")
            sys.exit(4)
        else:
            print_error("The provided host is not an IP nor a valid Domain")
            return -1

    #if protohelp and verbose:
    #    host = "<HOST>" if not host else host
    #    port = "<PORT>" if not port else port
    #    username = "<USERNAME_REQ>" if not username else username
    #    password = "<PASSWORD_REQ>" if not password else password
    #    ipv6 = "<IPv6_REQ>" if not ipv6 else ipv6
    #    domain = "<DOMAIN_REQ>" if not domain else domain
    #    path = "</SOME/PATH>" if not path else path

    if protohelp and verbose:
        host = "<HOST>"
        port = "<PORT>"
        username = "<USERNAME_REQ>"
        ulist = "<USERNAMES_LIST"
        password = "<PASSWORD_REQ>"
        plist = "<PASSWORDS_LIST>"
        ipv6 = "<IPv6_REQ>"
        domain = "<DOMAIN_REQ>"
        path = "</SOME/PATH>"
        extensions = "<extensions(php,asp,html)>"
        
    if proto in valid_protos.keys():
        warrior = Ajp_warrior(host, port, workdir, valid_protos[proto], intensity, username, ulist, password, plist, notuse, extensions,
                              path, reexec,
                              ipv6, domain, interactive, verbose, executed, exec)

    if protohelp:
        warrior.print_help()
    else:
        if not interactive:
            warrior.run()
        else:
            return warrior
