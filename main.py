import os
import requests
import json
import urllib3
import time

print("\033[96mRunning script at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\033[0m")

# Define all environment variables at the top
CONTAINER_NAME = os.environ["CONTAINER_NAME"]
PORTAINER_PAT = os.environ["PORTAINER_PAT"]
PORTAINER_URL = os.environ["PORTAINER_URL"]
INSTANCE_ID = int(os.environ["INSTANCE_ID"])
NETWORK_NAME = os.environ["NETWORK_NAME"]
SAVE_RESPONSE = (os.environ["SAVE_RESPONSE"] == "True")
OUT_FILE_NAME = os.environ["OUT_FILE_NAME"]

try:
    if os.path.isfile(".env"):
        print("\033[91mWarning:\033[0m Found .env file. \033[91mRunning in local mode.\033[0m")
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
print(f"Set Headers:")
print(json.dumps(headers, indent=4))

response = requests.get(f"{PORTAINER_URL}/api/endpoints/{INSTANCE_ID}/docker/containers/json", headers=headers, verify=False)
data = list(response.json())
print("Getting container data:")
print(f"\t{response.status_code, response.text if response.status_code != 200 else "OK"}")

container = list(filter(lambda x: x["Names"][0] == CONTAINER_NAME, data))[0]
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
    print(connect_response.status_code, connect_response.text)

# Write the response to a JSON file
if SAVE_RESPONSE:
    with open(OUT_FILE_NAME, 'w') as f:
        json.dump(response.json(), f, indent=4)