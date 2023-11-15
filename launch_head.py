# launch.py
# Usage: python launch.py --exp-name test --command "rllib train --run PPO --env CartPole-v0"

import argparse
import subprocess
import sys
import time

from pathlib import Path

def get_hostname(jobid):
    hostname_found = False
    while not hostname_found:

        command = f"squeue -h -j {jobid} -o '%N'"
        hostname = subprocess.run(command, capture_output=True, text=True, shell=True)
        if hostname.returncode == 0 and hostname.stdout.strip() != "":
            hostname = hostname.stdout.strip()
            hostname_found = True

        time.sleep(1)

    return hostname

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exp-name", type=str, required=True,
        help="The job name and path to logging file (exp_name.log)."
    )
    parser.add_argument(
        "--num-nodes", "-n", type=int, default=1,
        help="Number of nodes to use."
    )

    args = parser.parse_args()

    job_name = f'{args.exp_name}_{time.strftime("%m%d-%H%M", time.localtime())}'

    command = f"sbatch --parsable head.sh"
    jobid = subprocess.run(command, capture_output=True, text=True, shell=True)

    if jobid.returncode == 0:
        jobid = jobid.stdout.strip()
        print("jobid:", jobid)
    else:
        raise Exception("Error:", jobid.stderr.strip())

    header_hostname = get_hostname(jobid)

    print("header_hostname:", header_hostname)