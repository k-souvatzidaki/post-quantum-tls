sudo mkdir /etc/nginx/certs/

# generate server certificate with dilithium
sudo openssl req -x509 -new -newkey dilithium3 -keyout /etc/nginx/certs/dilithium3_CA.key -out /etc/nginx/certs/dilithium3_CA.crt -nodes -subj "/CN=10.0.0.1" -days 365 -config  /usr/local/ssl/openssl.cnf
sudo openssl genpkey -algorithm dilithium3 -out /etc/nginx/certs/dilithium3_srv.key
sudo openssl req -new -newkey dilithium3 -keyout /etc/nginx/certs/dilithium3_srv.key -out /etc/nginx/certs/dilithium3_srv.csr -nodes -subj "/CN=10.0.0.1" -config /usr/local/ssl/openssl.cnf
sudo openssl x509 -req -in /etc/nginx/certs/dilithium3_srv.csr -out /etc/nginx/certs/dilithium3_srv.crt -CA /etc/nginx/certs/dilithium3_CA.crt -CAkey /etc/nginx/certs/dilithium3_CA.key -CAcreateserial -days 365

# generate server certificate with CROSS
sudo openssl req -x509 -new -newkey mayo3 -keyout /etc/nginx/certs/mayo3_CA.key -out /etc/nginx/certs/mayo3_CA.crt -nodes -subj "/CN=10.0.0.1" -days 365 -config  /usr/local/ssl/openssl.cnf
sudo openssl genpkey -algorithm mayo3 -out /etc/nginx/certs/mayo3_srv.key
sudo openssl req -new -newkey mayo3 -keyout /etc/nginx/certs/mayo3_srv.key -out /etc/nginx/certs/mayo3_srv.csr -nodes -subj "/CN=10.0.0.1" -config /usr/local/ssl/openssl.cnf
sudo openssl x509 -req -in /etc/nginx/certs/mayo3_srv.csr -out /etc/nginx/certs/mayo3_srv.crt -CA /etc/nginx/certs/mayo3_CA.crt -CAkey /etc/nginx/certs/mayo3_CA.key -CAcreateserial -days 365

# generate server certificate with MAYO
sudo openssl req -x509 -new -newkey CROSSrsdp128balanced -keyout /etc/nginx/certs/CROSSrsdp128balanced_CA.key -out /etc/nginx/certs/CROSSrsdp128balanced_CA.crt -nodes -subj "/CN=10.0.0.1" -days 365 -config  /usr/local/ssl/openssl.cnf
sudo openssl genpkey -algorithm CROSSrsdp128balanced -out /etc/nginx/certs/CROSSrsdp128balanced_srv.key
sudo openssl req -new -newkey CROSSrsdp128balanced -keyout /etc/nginx/certs/CROSSrsdp128balanced_srv.key -out /etc/nginx/certs/CROSSrsdp128balanced_srv.csr -nodes -subj "/CN=10.0.0.1" -config /usr/local/ssl/openssl.cnf
sudo openssl x509 -req -in /etc/nginx/certs/CROSSrsdp128balanced_srv.csr -out /etc/nginx/certs/CROSSrsdp128balanced_srv.crt -CA /etc/nginx/certs/CROSSrsdp128balanced_CA.crt -CAkey /etc/nginx/certs/CROSSrsdp128balanced_CA.key -CAcreateserial -days 365
