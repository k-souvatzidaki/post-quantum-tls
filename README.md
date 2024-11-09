# Post-quantum TLS
An experiment for post-quantum algorithms using Open Queantum Safe OpenSSL provider
https://github.com/open-quantum-safe/liboqs 
https://github.com/open-quantum-safe/oqs-provider 

## Set-up
Server and client run on separate machines with Ubuntu 24.04.1 operating system 
On both machines run the commands in configure.sh to prepare an oqs-enabled installation of OpenSSL with oqs-provider

## Server
- Use the confioguration file in server/openssl.cnf for the OpenSSL installation
- Generate server certificate signed with Dilithium using the commands in server/gencrt.sh
- Run the command in server/init.sh to start a server with the Dilithium certificate and Kyber as the public key-exchange algorithm 

## Client 
- Run the command in client/init.sh to start a connection to the server with Kyber as the public key-exchange algorithm 