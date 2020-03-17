FROM kalilinux/kali-rolling

COPY . /legion

# Install legion dependencies.
RUN apt-get update
RUN apt-get install -y \
        cewl \
        curl \
        davtest \
        dnsrecon \
        dnsutils \
        enum4linux \
        finger \
        git \
        hydra \
        ike-scan \
        metasploit-framework \
        netcat \
        nfs-common \
        nmap \
        ntp \
        oscanner \
        python2 \
        python3 \
        python3-ldapdomaindump \
        python3-pip \
        python-pip \
        smbclient \
        smbmap \
        snmp \
        sqlmap \
        sslscan \
        sslyze

# Start the installation phase.
RUN cd legion/git/ && ./install.sh

WORKDIR /legion
CMD /usr/bin/python3 legion.py
