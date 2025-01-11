# start a test server with dilithium certificate 
openssl s_server -cert dilithium3_srv.crt -key dilithium3_srv.key -www -tls1_3 -groups openssl s_client -connect 172.20.10.11:443 -tls1_3 -groups x25519_kyber768
