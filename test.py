#!/usr/bin/env python3

import paramiko
import pandas as pd
from tqdm.contrib.concurrent import thread_map
import time
import re
import os

machine_ips = [
  "130.216.216.179",
  "130.216.216.196",
  "130.216.217.65",
  "130.216.217.127",
  "130.216.216.117",
  "130.216.216.201"
]

# Define the command to be executed on each machine
command = './tf_devices.py & sleep 10s && time nvidia-smi -q'

# Function to SSH into a machine, run the command, and measure time
def execute_ssh(ip):
    start_time = time.time()
    try:
      # SSH into the machine using the provided SSH key
      private_key_path = '/home/ubuntu/.ssh/id_rsa'
      private_key = paramiko.RSAKey(filename=private_key_path)

      # SSH into the machine
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(ip, username='ubuntu', pkey=private_key)

      # Run the command and measure time
      stdin, stdout, stderr = ssh.exec_command(command, timeout=300)
      stdout.channel.set_combine_stderr(True)
      output = stdout.read().decode('utf-8', errors="replace")

      # Close the SSH connection
      ssh.close()
    except Exception as e:
       output = str(e)
    elapsed_time = time.time() - start_time
    return ip, elapsed_time, output


# Execute SSH commands in parallel with tqdm's thread_map
results = list(thread_map(execute_ssh, machine_ips))

# Create a DataFrame from the results
df = pd.DataFrame(results, columns=['IP', 'time', 'output'])
df['timestamp'] = pd.Timestamp.now()

# Save results to a CSV file using pandas
csv_filename = 'ssh_results.csv'
if os.path.isfile(csv_filename):
  df = pd.concat([pd.read_csv(csv_filename, on_bad_lines="warn"), df])
df.to_csv(csv_filename, index=False)

print(f"Results saved to {csv_filename}")
