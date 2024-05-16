"""
This script is used to interact with the Portainer API to manage Docker containers. 

It fetches the details of a specific Docker container, checks the networks that the container is connected to, and connects the container to a specific network if it's not already connected.

Environment Variables:
- CONTAINER_NAME: The name of the Docker container to manage.
- PORTAINER_PAT: The Personal Access Token for the Portainer API.
- PORTAINER_URL: The URL of the Portainer API.
- INSTANCE_ID: The ID of the Portainer instance to interact with.
- NETWORK_NAME: The name of the network to connect the container to.
- SAVE_RESPONSE: Whether to save the API response to a file (True/False).
- OUT_FILE_NAME: The name of the file to save the API response to.

The script can run in two modes:
- Local mode: If a .env file is found in the same directory, the script will load environment variables from this file.
- Container mode: If no .env file is found, the script will load environment variables from the system environment.

In both modes, if a required environment variable is missing, the script will exit with an error message. If an optional environment variable is missing, the script will continue running with a default value.

The script prints the status of each operation to the console, and optionally saves the API response to a file.
"""

import os
import requests
import json
import urllib3
import time

print("\033[96mRunning script on " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\033[0m at \033[96m" + os.path.dirname(os.path.abspath(__file__)) + "\033[0m")

# Define all environment variables at the top
try:
    CONTAINER_NAME = os.environ["CONTAINER_NAME"]
    PORTAINER_PAT = os.environ["PORTAINER_PAT"]
    PORTAINER_URL = os.environ["PORTAINER_URL"]
    INSTANCE_ID = int(os.environ["INSTANCE_ID"])
    NETWORK_NAME = os.environ["NETWORK_NAME"]
    SAVE_RESPONSE = (os.environ["SAVE_RESPONSE"] == "True")
    OUT_FILE_NAME = os.environ["OUT_FILE_NAME"]
except KeyError as e:
    # Check if the missing environment variable is required or not
    if e.args[0] in ['OUT_FILE_NAME', 'INSTANCE_ID', 'SAVE_RESPONSE']:
        print("\033[38;5;208m" + "Warning:" + "\033[0m " + f"Missing environment variable: {e}")
        # Set default values for optional variables
        if e.args[0] == 'OUT_FILE_NAME':
            OUT_FILE_NAME = "_container_data.json"
            print(f"Since this variable is not required, the script will continue without it. Defaulting to str:_container_data.json")
        if e.args[0] == 'INSTANCE_ID':
            INSTANCE_ID = 1
            print(f"Since this variable is not required, the script will continue without it. Defaulting to int:1")
        if e.args[0] == 'SAVE_RESPONSE':
            SAVE_RESPONSE = False
            print(f"Since this variable is not required, the script will continue without it. Defaulting to bool:False")
    else:
        # Exit if required environment variable is missing
        print("\033[91m" + "Error:" + "\033[0m " + f"Missing environment variable: {e}")
        print(f"Since {e} is required, the script will exit.")
        exit(1)
try:
    if os.path.isfile(".env"):
        # Check if .env file exists and load it
        print("\033[38;5;208mWarning:\033[0m Found .env file. \033[38;5;208mRunning in local mode.\033[0m")
        # Load .env file for testing
        from dotenv import load_dotenv
        load_dotenv()
    else:
        print("No .env file found. \033[91mRunning in container mode.\033[0m")
except:
    print("Error loading .env file. \033[91mRunning in container mode.\033[0m")

# Disable: InsecureRequestWarning: Unverified HTTPS request is being made to host. (Since this is a private network.)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "X-API-Key": PORTAINER_PAT
}
# print(f"Set Headers:")
# print(json.dumps(headers, indent=4))

response = requests.get(f"{PORTAINER_URL}/api/endpoints/{INSTANCE_ID}/docker/containers/json", headers=headers, verify=False)
data = list(response.json())
print("Getting container data:")
print(f"\t{response.status_code, response.text if response.status_code != 200 else "OK"}")

# Find the container by name
container = filter(lambda x: x["Names"][0] == CONTAINER_NAME, data)
if not container:
    print(f"\033[91mContainer {CONTAINER_NAME.removeprefix('/')} not found.\033[0m \nExiting.")
    exit(1)
container = list(container)[0]
networks = container["NetworkSettings"]["Networks"]
networks =  [network for network in networks]
print(f"\033[95m{len(networks)}\033[0m networks found for container: \033[95m{CONTAINER_NAME.removeprefix("/")}\033[0m: {", ".join(networks)}")

if NETWORK_NAME not in networks:
    print(f"{NETWORK_NAME} not found for container.\nAdding network {NETWORK_NAME} to container {CONTAINER_NAME.removeprefix('/')}")
    connect_data = {
        "Container": container["Id"],
        "EndpointConfig": {}
    }
    connect_response = requests.post(f"{PORTAINER_URL}/api/endpoints/{INSTANCE_ID}/docker/networks/{NETWORK_NAME}/connect", headers=headers, json=connect_data, verify=False)
    print(f"\t{connect_response.status_code, connect_response.text if connect_response.status_code != 200 else "OK"}")
else:
    print(f"{NETWORK_NAME} found for container. \033[92mNo action needed.\033[0m")
# Write the response to a JSON file
if SAVE_RESPONSE:
    with open(OUT_FILE_NAME, 'w') as f:
        json.dump(response.json(), f, indent=4)