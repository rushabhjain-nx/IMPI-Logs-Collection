# Cluster IPMI SEL logs

This Python script fetches IPMI logs from all nodes in a cluster via SSH and stores them in separate folders for each cluster. The script requires the root password for SSH access to the hosts.
Developed by Rushabh Jain (rushabh.jain@nutanix.com)

## Features

- Connects to multiple nodes in a cluster using SSH.
- Fetches IPMI logs from each node.
- Stores logs in separate directories for each cluster.

## Requirements

- Python 3.8 >= 
- Root password for Hosts
- Cluster Credentials (Prism Element)

## Setup

1. Download the script files on your system along with the requirements.

2. Create a virtual environment (optional but recommended):

    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip3 install -r requirements.txt
    ```

## Usage



1. Run the script:

    ```
    python3 sel_logs_script.py
    ```

2. Follow the prompts to enter cluster credentials and root password.

3. The script will fetch the IPMI logs from all nodes and store them in separate folders named after the clusters.
