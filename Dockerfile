FROM kalilinux/kali

COPY . /legion

# Install system dependencies.
RUN apt-get update
RUN apt-get install -y \
        git \
        python2 \
        python-pip \
        python3 \
        python3-pip \
        nmap \
        metasploit-framework

# Start the installation phase.
RUN cd legion/git/ && ./install.sh

WORKDIR /legion
CMD /usr/bin/python3 legion.py
