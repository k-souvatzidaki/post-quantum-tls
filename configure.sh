### STEP 1: Install Openssl 3.4.0
# replace openssl version with latest (3.4.0)
sudo apt-get purge --auto-remove openssl
sudo apt-get autoremove
sudo apt-get autoclean

# install dependencies
sudo apt-get update && sudo apt-get upgrade
sudo apt install build-essential checkinstall zlib1g-dev ca-certificates -y

# fetch openssl source
cd /usr/local/src/
sudo wget https://www.openssl.org/source/openssl-3.4.0.tar.gz
sudo tar -xf openssl-3.4.0.tar.gz
cd openssl-3.4.0

# compile openssl
sudo ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib
sudo make
sudo make test
sudo make install

# configure link libraries
cd /etc/ld.so.conf.d/
sudo su
echo "/usr/local/ssl/lib64" >> openssl-3.4.0.conf
exit
sudo ldconfig -v

# configure openssl binary
sudo vim /etc/environment 
# add :/usr/local/ssl/bin to PATH
source /etc/environment
echo $PATH

openssl version 


### STEP 2: Build liboqs
# install dependencies
sudo apt install astyle cmake gcc ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz python3-yaml valgrind -y

# get liboqs source
cd ~
git clone https://github.com/open-quantum-safe/liboqs.git 
cd liboqs

# build liboqs
mkdir build && cd build
cmake -GNinja ..
ninja
sudo ninja install 

cd ..


### STEP 3: Build oqs-provider 
# install dependencies
sudo apt install cmake build-essential git -y

# get oqs-provider source
git clone https://github.com/open-quantum-safe/oqs-provider.git
cd oqs-provider

# build oqs-provider on openssl 3.4.0 installation and liboqs
sudo su
liboqs_DIR=../liboqs cmake -DOPENSSL_ROOT_DIR=/usr/local/ssl/ -S . -B _build && cmake --build _build && cmake --install _build 

