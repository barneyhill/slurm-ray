# launch.py
# Usage: python launch.py --exp-name test --command "rllib train --run PPO --env CartPole-v0"

import argparse
import subprocess
import os
import time

from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exp-name", type=str, required=True,
        help="The job name and path to logging file (exp_name.log)."
    )
    parser.add_argument(
        "--num-workers", "-n", type=int, default=1,
        help="Number of nodes to use."
    )
    parser.add_argument(
        "--head-ip", type=str, required=True,
        help="Head IP."
    )
    parser.add_argument(
        "--head-port", type=str, required=True,
        help="Head Port."
    )


    args = parser.parse_args()

    job_name = f'{args.exp_name}_{time.strftime("%m%d-%H%M", time.localtime())}'

    os.environ['HEAD_IP'] = args.head_ip
    os.environ['HEAD_PORT'] = args.head_port
    command = f"sbatch --array 1-{args.num_workers} worker.sh"
    subprocess.run(command, capture_output=True, text=True, shell=True)
