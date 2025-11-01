import subprocess
import time
import csv
import numpy as np
import os 
import shutil


# FUNCTIONS
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
        'delay', "0ms",
        'rate', '1000mbit'
    ]

    result = subprocess.run(command, text=True, timeout=10, input="", stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return result


def write_in_csv(path, row):

    try:
        with open(path, 'a', newline='') as out:
            writer = csv.writer(out, delimiter=";")
            writer.writerow(list(row))

    except Exception as e:
        print(f'Error writing line {row} in {path}: {e}')
        exit(1)



# STATIC VARS
# Key exchange algorithms: KYBER, BIKE, HQC
_KEMS = [
    # classical ECDH 
    "prime256v1",
    "secp384r1",
    "secp521r1",
    # POST QUANTUM 
    "kyber512", 
    "kyber768", 
    "kyber1024", 
    "hqc128", 
    "hqc192", 
    "hqc256",
    "bikel1",
    "bikel3",
    "bikel5",
    # HYBRID
    "p256_kyber512", 
    "p384_kyber768", 
    "p256_kyber768", 
    "p521_kyber1024",
    "p256_hqc128", 
    "p384_hqc192",  
    "p521_hqc256", 
    "p256_bikel1",  
    "p384_bikel3", 
    "p521_bikel5"
]

# Digital signature algorithm: DILITHIUM
_CERT_CIPHER = "dilithium3"
_CERT_FILE = "/etc/nginx/certs/dilithium3_srv.crt"

# Configuration
_PORT = 443
_ITERATIONS = 1000
_PKT_LOSS_RANGE = [0,1,3,6,10]

# results files: RESULTS_std_deviation.csv, RESULTS_box_plot.csv, RESULTS_all.csv
_RESULTS_PATH_STD = "results/RESULTS_std_deviation.csv"
_RESULTS_PATH_BOX = "results/RESULTS_box_plot.csv"
_RESULTS_PATH_ALL = "results/RESULTS_all.csv"
_RESULTS_DIR = "results" 


# MAIN
if __name__ == '__main__':
    
    if os.path.exists(_RESULTS_DIR):
        shutil.rmtree(_RESULTS_DIR)

    os.mkdir(_RESULTS_DIR)


    # for all packet loss ratio values, create a new table inside the files
    for pkt_loss in _PKT_LOSS_RANGE:

        # create headers in files for new table per packet loss
        write_in_csv(_RESULTS_PATH_STD, ["cipher", "mean", "std_deviation", f"pkt_loss = {pkt_loss}"])
        write_in_csv(_RESULTS_PATH_BOX, ["cipher", "value", f"pkt_loss = {pkt_loss}"])
        write_in_csv(_RESULTS_PATH_ALL, ["cipher", "mean", "std_deviation", "min", "25th_percentile", "median", "75th_percentile", "max", "95th_percentile", f"pkt_loss = {pkt_loss}"])

        # add packet loss inside network
        run_qdisk_command("srv_ns", "srv_ve", pkt_loss)
        run_qdisk_command("cli_ns", "cli_ve", pkt_loss)

        for kem in _KEMS:

            total_times = []
            print(f"Running for packet loss: {pkt_loss} with cipher: {kem}")

            # new experiment
            for i in range (0, _ITERATIONS):

                start_time = time.time() # start counter
                try:
                    result = run_sclient_command(_PORT, _CERT_FILE, kem) # initiate tls handshake
                    
                    end_time = time.time() # end counter
                    duration = end_time - start_time # calculate duration

                    total_times.append(duration)

                    if result.stderr:
                        print("Error Output:", result.stderr)

                except Exception as e:
                    print("Unexpected error:", str(e))
            

            # calcualate statistics and write in file
            total_times_nparray = np.array(total_times)
            
            mean = np.mean(total_times_nparray)
            standard_deviation = np.std(total_times_nparray)
            minimum = np.min(total_times_nparray)
            percentile_25 = np.percentile(total_times_nparray, 25)
            median = np.percentile(total_times_nparray, 50)
            percentile_75 = np.percentile(total_times_nparray, 75)
            maximum = np.max(total_times_nparray)
            percentile_95 = np.percentile(total_times_nparray, 95)


            print(f"Results: mean - {mean}, standard_deviation - {standard_deviation}, minimum - {minimum}, 25th percentile - {percentile_25}, median - {median}, 75th percentile - {percentile_75}, maximum - {maximum}, 95th percentile - {percentile_95}")

            # write values for barchart
            write_in_csv(_RESULTS_PATH_STD, [kem, mean, standard_deviation])

            # write values for box plot
            write_in_csv(_RESULTS_PATH_BOX, [kem, minimum])
            write_in_csv(_RESULTS_PATH_BOX, [kem, percentile_25])
            write_in_csv(_RESULTS_PATH_BOX, [kem, median])
            write_in_csv(_RESULTS_PATH_BOX, [kem, percentile_75])
            write_in_csv(_RESULTS_PATH_BOX, [kem, maximum])

            # write values for tables/plots
            write_in_csv(_RESULTS_PATH_ALL, [kem, mean, standard_deviation, minimum, percentile_25, median, percentile_75, maximum, percentile_95])


        # Blank line between runs
        write_in_csv(_RESULTS_PATH_STD, [])
        write_in_csv(_RESULTS_PATH_BOX, [])
        write_in_csv(_RESULTS_PATH_ALL, [])