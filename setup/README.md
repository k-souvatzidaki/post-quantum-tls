# Environment Setup

## Prerequisites 

## Network Namespaces
Run sudo /bin/bash setup_ns.sh 

## Configurations 
### Openssl config 
sudo rm -f /usr/local/ssl/openssl.cnf
sudo nano /usr/local/ssl/openssl.cnf
openssl list -providers

### Nginx config
sudo rm -f /etc/nginx/nginx.conf
sudo nano /etc/nginx/nginx.conf

## Generate certificates 
Run gencrt.sh


## Start Nginx in server namespace 
sudo ip netns exec srv_ns nginx 
sudo ip netns exec cli_ns telnet 10.0.0.1 4431