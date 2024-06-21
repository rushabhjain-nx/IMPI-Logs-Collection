import requests
import json
import csv
import os
from getpass import getpass
import urllib3
import paramiko




# Author : Rushabh Jain (rushabh.jain@nutanix.com)
cluster_name = ""
def ssh_command(ip, username, password, command):
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        
        ssh_client.connect(ip, username=username, password=password)

        stdin, stdout, stderr = ssh_client.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            print(f"Error occurred: {error}")
            return None
        else:
            return output
           

    except paramiko.AuthenticationException:
        print("Authentication failed, please check the host password (root user) for ", ip)
        return None
    except paramiko.SSHException as e:
        print(f"SSH error: {str(e)}")
        return None
    finally:
        ssh_client.close()

def get_cluster_name(ip, username, password):
    url = f"https://{ip}:9440/PrismGateway/services/rest/v2.0/clusters/"
    headers = {"Content-Type": "application/json"}
    user = username
    passw = password
    urllib3.disable_warnings()
    try:
        response = requests.get(url, headers=headers, auth=(user, passw), verify=False)
        if response.status_code == 200:
            data = response.json()["entities"]
            global cluster_name
            cluster_name = data[0]["name"]
            return 1
        else:
            #print(f"Failed to get cluster name. Status code: {response.status_code}")
            
            return None
    except:
        return None

def get_host_ips(ip, username, password):
    url = f"https://{ip}:9440/PrismGateway/services/rest/v2.0/hosts/"
    headers = {"Content-Type": "application/json"}
    user = username
    passw = password
    urllib3.disable_warnings()
    try : 
        response = requests.get(url, headers=headers, auth=(user, passw), verify=False)
    # print(response)
        if response.status_code == 200:
            data = {}
            hosts = response.json()["entities"]

            for obj in hosts:
                data[obj["name"]] = obj["hypervisor_address"]

            sorted_data = sorted(data.items(), key=lambda x: x[0])
            with open("hosts.json", "w") as outfile:
                json.dump(sorted_data, outfile, indent=4)
        # host_ips = [host["ipAddress"] for host in hosts]
            return 1
        else:
            return None
    except:
        return None


def main():
    while True:
        print()
        ip = input("Enter Prism Element IP: ").strip()
        username = input("Enter Prism Element Username: ").strip()
        password = getpass("Enter Prism Element Password: ").strip()
        res = get_cluster_name(ip, username, password)
        if res == 1:
            break
        else:
            print()
            print("Login failed. Please try again or check your credentials.")



    host_password = getpass("Enter Host Password (for Root user): ")
    print()
    print("Gathering Hosts details...")
    res = get_host_ips(ip, username, password)
    
    with open("hosts.json", "r") as f:
        host_ips = json.load(f)
    print("Data fetched : " ,host_ips)
    print()
    output_dir = cluster_name
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if not exists

    flag =0
    for obj in host_ips:
        host_name = obj[0]
        host_ip = obj[1]
        log_output = ssh_command(host_ip, "root", host_password, "ipmitool sel list")
        if log_output:
            file_name = f"{host_name}_{host_ip}.txt"
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, "w") as logfile:
                logfile.write(log_output)
            print(f"Logs fetched from {host_name} ({host_ip}) and stored in {file_name}")
        else:
            flag+=1
            print(f"Failed to fetch logs from {host_name} ({host_ip})")

    if flag==0:
        print("All host logs fetched and stored in 'output' directory")


if __name__ == "__main__":
    main()
