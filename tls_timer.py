import subprocess
import time
import csv


# Define the command
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

def run_qdisk_command(ns_name, ns_veth, pkt_loss):
    command = [
        'ip', 'netns', 'exec', ns_name,
        'tc', 'qdisc', 'change',
        'dev', ns_veth, 'root', 'netem',
        'limit', '1000',
        'loss', '{0}%'.format(pkt_loss),
        'rate', '1000mbit'
    ]

    result = subprocess.run(command, text=True, timeout=10, input="", stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return result


# Key exchange algorithms: KYBER, BIKE, HQC
# Signatures: DILITHIUM, CROSS, MAYO
kem_algorithms = [
    "kyber512", 
    # "p256_kyber512", 
    # "x25519_kyber512", 
    # "kyber768", 
    # "p384_kyber768", 
    # "x448_kyber768", 
    # "x25519_kyber768", 
    # "p256_kyber768", 
    # "kyber1024", 
    # "p521_kyber1024",
    # "hqc128", 
    # "p256_hqc128", 
    # "x25519_hqc128", 
    # "hqc192", 
    # "p384_hqc192", 
    # "x448_hqc192", 
    # "hqc256", 
    # "p521_hqc256",
    # "bikel1", 
    # "p256_bikel1", 
    # "x25519_bikel1", 
    # "bikel3", 
    # "p384_bikel3", 
    # "x448_bikel3", 
    # "bikel5", 
    # "p521_bikel5"
]

certificates = [
    {
        "port": 4431,
        "certificate_file": "/etc/nginx/certs/dilithium3_srv.crt",
        "algorithm": "dilithium3"
    },
    # {
    #     "port": 4432,
    #     "certificate_file": "/etc/nginx/certs/mayo3_srv.crt",
    #     "algorithm": "mayo3", 
    # },
    # {
    #     "port": 4433,
    #     "certificate_file": "/etc/nginx/certs/CROSSrsdp128balanced_srv.crt",
    #     "algorithm": "CROSSrsdp128balanced"
    # }
]

iterations = 1000

if __name__ == '__main__':

    for certificate in certificates: 
        port = certificate["port"]
        certificate_file = certificate["certificate_file"]

        print("now running using certificate: ", certificate["algorithm"])
        with open(f'data/{certificate["algorithm"]}.csv','w') as out:
            fieldnames = [' '] + kem_algorithms
            print(fieldnames)
            writer = csv.DictWriter(out, delimiter=";", fieldnames=fieldnames)
            writer.writeheader()

            for pkt_loss in [0, 0.1, 0.5, 1, 1.5, 2, 2.5, 3]:
                # insert packet loss
                run_qdisk_command("srv_ns", "srv_ve", pkt_loss)
                run_qdisk_command("cli_ns", "cli_ve", pkt_loss)

                row = {
                    " ": pkt_loss
                }

                for kem in kem_algorithms:
                    total_time = 0

                    for i in range (0, iterations):
                        start_time = time.time()
                        try:
                            result = run_sclient_command(port, certificate_file, kem)
                            end_time = time.time()

                            total_time += end_time - start_time

                            if result.stderr:
                                print("Error Output:", result.stderr)

                        except Exception as e:
                            print("Unexpected error:", str(e))
                    
                    # Print average execution time
                    print(f"KEM: {kem} - Execution Time: {total_time/iterations:.3f} seconds")
                    row[kem] = total_time/iterations
                    # writer.writerow({'kem': kem, 'pkt_loss': pkt_loss, 'time': total_time/iterations})
                
                writer.writerow(row)


