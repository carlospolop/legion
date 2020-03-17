FROM alpine:latest

COPY . /legion

# Install system dependencies.
RUN apk add bash
RUN apk add git
RUN apk add python3
RUN apk add nmap

# Start the installation phase.
RUN cd legion/git/ && ./install.sh

WORKDIR /legion
CMD /usr/bin/python3 legion.py
