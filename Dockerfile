FROM alpine:latest

COPY . /legion

RUN apk add bash
RUN apk add git
RUN apk add python3
RUN apk add nmap
RUN cd legion/git/ && ./install.sh

WORKDIR /legion
CMD /usr/bin/python3 legion.py
