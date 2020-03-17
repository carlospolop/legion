FROM kalilinux/kali-rolling

COPY . /legion

# Install legion dependencies.
RUN apt-get update
RUN apt-get install -y \
        git \
        python2 \
        python-pip \
        python3 \
        python3-pip \
        python3-ldapdomaindump \
        nmap \
        ike-scan \
        sqlmap \
        hydra \
        snmp \
        netcat \
        curl \
        davtest \
        dnsutils \
        dnsrecon \
        sslyze \
        smbmap \
        enum4linux \
        smbclient \
        sslscan \
        oscanner \
        finger \
        nfs-common \
        ntp \
        cewl \
        metasploit-framework

# Start the installation phase.
RUN cd legion/git/ && ./install.sh

WORKDIR /legion
CMD /usr/bin/python3 legion.py
