import subprocess
import time
import csv
import numpy as np


# Run netns commands
def run_sclient_command(port, certificate, kem_algorithm): 
    command = [
        "ip", "netns", "exec", "cli_ns",
        "openssl", "s_client",
        "-connect", f"10.0.0.1:{port}",
        "-tls1_3",
        "-groups", kem_algorithm,
        "-CAfile", certificate
    ]
    result = subprocess.run(command, text=True, timeout=10, input="", stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return result

def run_qdisk_command(ns_name, ns_veth, pkt_loss, delay_ms):
    command = [
        'ip', 'netns', 'exec', ns_name,
        'tc', 'qdisc', 'change',
        'dev', ns_veth, 'root', 'netem',
        'limit', '1000',
        'loss', '{0}%'.format(pkt_loss),
        'delay', delay_ms,
        'rate', '1000mbit'
    ]

    result = subprocess.run(command, text=True, timeout=10, input="", stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return result


# Key exchange algorithms: KYBER, BIKE, HQC
# Signatures: DILITHIUM 
kem_algorithms = [
    "kyber512", 
    "p256_kyber512", 
    "kyber768", 
    "p384_kyber768", 
    "p256_kyber768", 
    "kyber1024", 
    "p521_kyber1024",
    "hqc128", 
    "p256_hqc128", 
    "hqc192", 
    "p384_hqc192", 
    "hqc256", 
    "p521_hqc256",
    "bikel1", 
    "p256_bikel1",  
    "bikel3", 
    "p384_bikel3", 
    "bikel5", 
    "p521_bikel5",
    "prime256v1",
    "secp384r1",
    "secp521r1"
]

certificates = [
    {
        "port": 443,
        "certificate_file": "/etc/nginx/certs/dilithium3_srv.crt",
        "algorithm": "dilithium3"
    }
]

iterations = 500

if __name__ == '__main__':

    for certificate in certificates: 
        port = certificate["port"]
        certificate_file = certificate["certificate_file"]
        delay_ms = '0ms'

        print("now running using certificate: ", certificate["algorithm"], "with delay: ", delay_ms)
        with open(f'data/{certificate["algorithm"]}_50th.csv','w') as out1, open(f'data/{certificate["algorithm"]}_95th.csv','w') as out2:
            fieldnames = [' '] + kem_algorithms
            writer1 = csv.DictWriter(out1, delimiter=";", fieldnames=fieldnames)
            writer1.writeheader()

            writer2 = csv.DictWriter(out2, delimiter=";", fieldnames=fieldnames)
            writer2.writeheader()

            for pkt_loss in [0, 0.1, 0.5, 1, 1.5, 2, 2.5, 3, 4, 6, 8, 10, 12, 14]:
                # insert packet loss
                run_qdisk_command("srv_ns", "srv_ve", pkt_loss, delay_ms)
                run_qdisk_command("cli_ns", "cli_ve", pkt_loss, delay_ms)

                row_50 = {
                    " ": pkt_loss
                }

                row_95 = {
                    " ": pkt_loss
                }


                for kem in kem_algorithms:
                    total_times = []

                    for i in range (0, iterations):
                        start_time = time.time()
                        try:
                            result = run_sclient_command(port, certificate_file, kem)
                            end_time = time.time()

                            total_times.append(end_time - start_time)

                            if result.stderr:
                                print("Error Output:", result.stderr)

                        except Exception as e:
                            print("Unexpected error:", str(e))
                    
                    # Print average execution time
                    percentile_50 = np.percentile(np.array(total_times), 50)
                    percentile_95 = np.percentile(np.array(total_times), 95)
                    print(f"KEM: {kem} - packet loss {pkt_loss} - delay {delay_ms} - Execution Time: 50th {percentile_50:.3f} 95th {percentile_95:.3f} seconds")
                    row_50[kem] = percentile_50
                    row_95[kem] = percentile_95
                
                writer1.writerow(row_50)
                writer2.writerow(row_95)