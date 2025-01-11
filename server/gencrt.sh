# generate server certificate with dilithium
openssl req -x509 -new -newkey dilithium3 -keyout dilithium3_CA.key -out dilithium3_CA.crt -nodes -subj "/CN=172.20.10.11" -days 365 -config  /usr/local/ssl/openssl.cnf
openssl genpkey -algorithm dilithium3 -out dilithium3_srv.key
openssl req -new -newkey dilithium3 -keyout dilithium3_srv.key -out dilithium3_srv.csr -nodes -subj "/CN=172.20.10.11" -config /usr/local/ssl/openssl.cnf
openssl x509 -req -in dilithium3_srv.csr -out dilithium3_srv.crt -CA dilithium3_CA.crt -CAkey dilithium3_CA.key -CAcreateserial -days 365
