#!/bin/bash

echo "[+] Installing odat"
git clone https://github.com/quentinhardy/odat.git odat
ln -s "$(pwd)/odat/odat.py" /usr/bin/odat.py

echo "[+] Installing ikeforce"
git clone https://github.com/SpiderLabs/ikeforce.git ikeforce
ln -s "$(pwd)/ikeforce/ikeforce.py" /usr/bin/ikeforce
pip2 install pyip pycrypto pyopenssl || pip install pyip pycrypto pyopenssl 

echo "[+] Installing rpcbind"
apt-get install rpcbind

echo "[+] Installing UDP-Proto-Scanner"
git clone https://github.com/portcullislabs/udp-proto-scanner.git udp-proto-scanner
cp udp-proto-scanner/udp-proto-scanner.pl udp-proto-scanner/udp-proto-scanner.conf /usr/local/bin

echo "[+] Installing snmp-mibs-downloader"
apt-get install snmp-mibs-downloader -y
sed -i 's/mibs :/#mibs :/g' /etc/snmp/snmp.conf

echo "[+] Creating symlink of /usr/share/doc/python-impacket/examples/samrdump.py"
ln -s /usr/share/doc/python-impacket/examples/samrdump.py /usr/bin/samrdump.py

echo "[+] Creating symlink of /usr/share/doc/python-impacket/examples/rpcdump.py"
ln -s /usr/share/doc/python-impacket/examples/rpcdump.py /usr/bin/rpcdump.py