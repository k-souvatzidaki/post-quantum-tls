# Environment Setup

## Prerequisites 

## Network Namespaces
Run the setup_ns script to create the client and server network namespaces inside the virtual machine 
```
sudo /bin/bash setup_ns.sh 
```

## Prerequisites
Install the following prerequisites to run the experiments
### 1. Install OpenSSL 3.4.0
First remove existing OpenSSL version to replace with latest (3.4.0)
```
sudo apt-get purge --auto-remove openssl -y
sudo apt-get autoremove -y && sudo apt-get autoclean -y
```

Then install dependencies to download latest OpenSSL version
```
sudo apt-get update && sudo apt-get upgrade -y
sudo apt install build-essential checkinstall zlib1g-dev ca-certificates -y
```

Fetch OpenSSL v3.4.0 source
```
cd /usr/local/src/
sudo wget https://www.openssl.org/source/openssl-3.4.0.tar.gz --no-check-certificate
sudo tar -xf openssl-3.4.0.tar.gz
cd openssl-3.4.0
```

Compile OpenSSL
```
sudo ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib
sudo make && sudo make install
```

Configure link libraries
```
cd /etc/ld.so.conf.d/
sudo su
echo "/usr/local/ssl/lib64" >> OpenSSL-3.4.0.conf
exit
sudo ldconfig -v
```

Configure OpenSSL binary by adding `:/usr/local/ssl/bin` to PATH variable. The variable is defined inside `/etc/environment` file
```
sudo vim /etc/environment 
```
Export PATH and verify
```
source /etc/environment
echo $PATH
```
Finally, check OpenSSL version, should be `3.4.0`
```
openssl version 
```

### 2. Build liboqs
The next step is to build the LibOQS library 
First, install some dependencies
```
sudo apt install astyle cmake gcc ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz python3-yaml valgrind -y
```

Download the LibOQS source
```
cd ~ && git clone https://github.com/open-quantum-safe/liboqs.git 
cd liboqs
```

Build LibOQS
```
mkdir build && cd build && cmake -GNinja .. && ninja
sudo ninja install 
cd ..
```

### 3. Build OQS Provider
Once LibOQS is compiled, we can install the OpenSSL provider
First, install some dependencies
```
sudo apt install cmake build-essential git -y
```

Get the oqs-provider source
```
git clone --branch 0.8.0 https://github.com/open-quantum-safe/oqs-provider.git && cd oqs-provider
```

Build oqs-provider on OpenSSL 3.4.0 installation using pre-built LibOQS
```
sudo su
liboqs_DIR=../liboqs cmake -DOPENSSL_ROOT_DIR=/usr/local/ssl/ -S . -B _build && cmake --build _build && cmake --install _build 
exit
```

### 4. Install Nginx
Finally, install the Nginx web server. Disable the service for now. 
```
sudo apt install nginx -y
sudo systemctl stop nginx && sudo systemctl disable nginx
```

## Configurations 
Once the network namespaces and all prerequisites are prepared, proceed with the following configurations
### 1. OpenSSL config
First remove any existing OpenSSL config
``` 
sudo rm -f /usr/local/ssl/openssl.cnf
```
Copy [setup/openssl.cnf](./openssl.cnf) inside the `/usr/local/ssl` directory. Verify using the command
```
openssl list -providers
```

### 2. Nginx config
Copy [setup/nginx.conf](./nginx.conf) inside the `/etc/nginx` directory


## 3. Generate certificates 
Run the following commands to generate DILITHIUM certificates 
```
cd ~
sudo mkdir /etc/nginx/certs/

sudo openssl req -x509 -new -newkey dilithium3 -keyout /etc/nginx/certs/dilithium3_CA.key -out /etc/nginx/certs/dilithium3_CA.crt -nodes -subj "/CN=10.0.0.1" -days 365 -config  /usr/local/ssl/openssl.cnf

sudo openssl genpkey -algorithm dilithium3 -out /etc/nginx/certs/dilithium3_srv.key

sudo openssl req -new -newkey dilithium3 -keyout /etc/nginx/certs/dilithium3_srv.key -out /etc/nginx/certs/dilithium3_srv.csr -nodes -subj "/CN=10.0.0.1" -config /usr/local/ssl/openssl.cnf

sudo openssl x509 -req -in /etc/nginx/certs/dilithium3_srv.csr -out /etc/nginx/certs/dilithium3_srv.crt -CA /etc/nginx/certs/dilithium3_CA.crt -CAkey /etc/nginx/certs/dilithium3_CA.key -CAcreateserial -days 365
```

## 4. Start Nginx in server namespace 
When everything is set up, start nginx in the server network namespace. Verify connectivity using telnet
```
sudo ip netns exec srv_ns nginx 
sudo ip netns exec cli_ns telnet 10.0.0.1 4431
```