sudo mkdir /etc/nginx/certs/

# generate server certificate with dilithium
sudo openssl req -x509 -new -newkey dilithium3 -keyout /etc/nginx/certs/dilithium3_CA.key -out /etc/nginx/certs/dilithium3_CA.crt -nodes -subj "/CN=10.0.0.1" -days 365 -config  /usr/local/ssl/openssl.cnf
sudo openssl genpkey -algorithm dilithium3 -out /etc/nginx/certs/dilithium3_srv.key
sudo openssl req -new -newkey dilithium3 -keyout /etc/nginx/certs/dilithium3_srv.key -out /etc/nginx/certs/dilithium3_srv.csr -nodes -subj "/CN=10.0.0.1" -config /usr/local/ssl/openssl.cnf
sudo openssl x509 -req -in /etc/nginx/certs/dilithium3_srv.csr -out /etc/nginx/certs/dilithium3_srv.crt -CA /etc/nginx/certs/dilithium3_CA.crt -CAkey /etc/nginx/certs/dilithium3_CA.key -CAcreateserial -days 365