# without client certificate 
openssl s_client -connect 172.20.10.11:443 -tls1_3 -groups x25519_kyber768