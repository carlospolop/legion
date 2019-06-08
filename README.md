# LEGION - Automatic vulnerability scanner

Legion is a tool that uses several well-known opensource tools to automatically, semi-automatically or manually scan for vulnerabilities and common misconfigurations of the most frequent found services running in machines that you could need to pentest.

Basically, the goal of Legion is to extract all information that you can extract from each service so you don't have to send the same commands all the time.
A lot of actions are repeated be being done by more than one tool, this is done to be sure that all the possible information is correctly extracted.

[![asciicast](https://asciinema.org/a/250539.png)](https://asciinema.org/a/250539)

## Installation

```sh
git clone https://github.com/carlospolop/legion.git /opt/legion
ln -s /opt/legion/legion.sh /usr/bin/legion
```


## Protocols Supported

You can get a list using the command `protos`

![](https://github.com/carlospolop/legion/blob/master/images/legion-protos.png)

## Brute force
All the protocols included in Legion that could be bruteforce, can be bruteforce using Legion. To see if a service can be brute forced and which command line will be used to do so (by default "hydra" is implemented, if hydra was not available metasploit or nmap will be used) set the protocol and the set the intensity to "3".

Example of brute forcing ssh:

![](https://github.com/carlospolop/legion/blob/master/images/legion-brute.png)

## Internal Commands

![](https://github.com/carlospolop/legion/blob/master/images/internal-commands.png)

Use the `help` internal command to get info about what each command does.

## Automatic Scann

Just lauch the internal command `startGeneral` and the '**General**' will start scanning ports and services automatically.

## Semi-Automatic Scann

You can set all the options properly and launch several commands to scan oe service. You can do this using the command `run`.

## Manual Scann

You can execute just one command using `exec <name>`. For example: `exec http_slqmap`

Some services has *on demand commands*, this commands can only be executed using this internal command (`exec`).

## Options

![](https://github.com/carlospolop/legion/blob/master/images/legion-options.png)

### domain

Set the domain of the DNS or of the user that you want to use

### extensions

Comma separeted list of possible extensions (to bruteforce files in a web server)

### host

Is the host that you want to attack (valid IP and domains)

Example:
```
set host 127.0.0.1
set host some.domain.com
```

### intensity

There are 3 intensities:
- **1**: Basic checks executed
- **2**: All chceks executed (Default)
- **3**: Brute force (check for availability)

### ipv6

Ipv6 address of the victim, could be usefull for some commands

### notuse

You can set a list (separated by commands) of commands that you don't want to use. For example, if you don't want modules from metasploit to be executed:`set notuse msf`.

### password

Set here the password of the username you want to use.

### path

Web server file path

### plist

Set here the path to a list of passwords (by default LEGION has its own list)

### port

The port where the service is running. If "0", then the default port of the service will be used (you can see this information using `info`)

### proto

Is the protocol that you want to attack

Example: 
```
set proto http
```

### reexec

Set `True` if you want already executed commands to be executed again (by default is set to False).

### ulist

Set a value here if you want to brute force a list of usernames (by default LEGION has its own list of usernames)

### username

Set the username of the user that you want to use/brute-force(by default to brute-force a list of users is used).


### verbose

If `True` the output of the command will be displayed as soon as it ends. If `False` it won't.

If `True` the output of `info` will show where each parameter is used, for example:

![](https://github.com/carlospolop/legion/blob/master/images/info-verbose-true.png)

If `False` the output of `info` will show the values of the parameters, for example:

![](https://github.com/carlospolop/legion/blob/master/images/info-verbose-false.png)

### workdir

Is the directory where the info of the victim is storaged. By default it is `$HOME/.legion`




