!/bin/bash

Y='\033[1;33m'
B='\033[0;34m'
G='\033[0;32m'
P='\033[1;35m'
NC='\033[0m'

function write_main(){
    printf "${G}[*]${Y} $1${NC}\n"
}

write_main "Installing basic python package"
pip3 install termcolor
echo ""

write_main "Installing odat"
git clone https://github.com/quentinhardy/odat.git odat
ln -s "$(pwd)/odat/odat.py" /usr/bin/odat.py
echo ""

write_main "Installing ikeforce"
git clone https://github.com/SpiderLabs/ikeforce.git ikeforce
ln -s "$(pwd)/ikeforce/ikeforce.py" /usr/bin/ikeforce
pip2 install pyip pycrypto pyopenssl || pip install pyip pycrypto pyopenssl
echo ""

write_main "Installing rpcbind"
apt-get install rpcbind
echo ""

write_main "Installing UDP-Proto-Scanner"
git clone https://github.com/portcullislabs/udp-proto-scanner.git udp-proto-scanner
cp udp-proto-scanner/udp-proto-scanner.pl udp-proto-scanner/udp-proto-scanner.conf /usr/local/bin
echo ""

write_main "Installing snmp-mibs-downloader"
apt-get install snmp-mibs-downloader -y
sed -i 's/mibs :/mibs :/g' /etc/snmp/snmp.conf
echo ""

write_main "Creating symlink of /usr/share/doc/python-impacket/examples/samrdump.py"
ln -s /usr/share/doc/python-impacket/examples/samrdump.py /usr/bin/samrdump.py
echo ""

write_main "Creating symlink of /usr/share/doc/python-impacket/examples/rpcdump.py"
ln -s /usr/share/doc/python-impacket/examples/rpcdump.py /usr/bin/rpcdump.py
echo ""

write_main "Intsalling dirsearch"
git clone https://github.com/maurosoria/dirsearch.git dirsearch
ln -s "$(pwd)/dirsearch/dirsearch.py" /usr/bin/dirsearch
echo ""

write_main "Installing dirhunt"
pip3 install dirhunt
echo ""

write_main "Installing Arjun"
git clone https://github.com/s0md3v/Arjun.git arjun
chmod +x arjun/arjun.py
echo ""
