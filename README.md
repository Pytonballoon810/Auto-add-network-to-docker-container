# Auto-add-network-to-docker-container
This Python script interacts with the Portainer API to manage Docker containers and networks. Here's a step-by-step breakdown of what it does:

1. **Setup**: It first sets up the Portainer URL, username, and API key, and defines the container and network details using the environment variables `PORTAINER_URL`, `PORTAINER_USERNAME`, `PORTAINER_PASSWORD`, `CONTAINER_NAME`, and `NETWORK_NAME`. `SAVE_RESPONSE` set to `True` you can save the response from the GET request to a JSON file.

2. **Get Containers**: It sends a GET request to the Portainer API to retrieve a list of all Docker containers. Set the `INSTANCE_ID` to define which docker environment to use (This can be found in the URL and must be a number, in most cases `1`). The response is converted to a list of dictionaries, where each dictionary represents a container.

3. **Find Container**: It filters the list of containers to find the one with the name specified in `CONTAINER_NAME`. It then retrieves the network settings for this container.

4. **Check Network**: It checks if the container is already connected to the network specified in `NETWORK_NAME`. If it's not, it proceeds to the next step.

5. **Connect to Network**: It sends a POST request to the Portainer API to connect the container to the network. It prints the status code and text of the response.

6. **Save Response**: If the `SAVE_RESPONSE` variable is set to `True`, it writes the response from the GET request (the list of all containers) to a JSON file named 'container_data.json' if not overwritten by `OUT_FILE_NAME`. If `SAVE_RESPONSE` is `False`, it skips this step.

# Usage

This service is meant to be run as a Docker container, so you may set the environment variables in the docker-compose file or in the command line. Although running it in docker is recommended, due to mainly using it regularly and on a scheduled basis, it is also possible to run it as a standalone script. For this define the environment variables in a `.env` file and run the script with `python3.12 main.py`.  
You will also need to install the required packages with `pip install -r requirements.txt` and run `pip install python-dotenv` manually as it is not required in the Docker container.
I would recommend creating a virtual environment for running this script locally especially if you have already installed other python versions than 3.12.

## Set up all environment variables. 
Remember to set ``PUID`` and ``PGID`` for security reasons.  
Here's a Markdown table of all the environment variables used in the script and their purposes:

| Environment Variable | Purpose |
| --- | --- |
| `CONTAINER_NAME` | The name of the container that the script is interacting with. |
| `PORTAINER_PAT` | The Personal Access Token (PAT) for Portainer, used for authentication. |
| `PORTAINER_URL` | The URL of the Portainer API that the script is interacting with. |
| `INSTANCE_ID` | The ID of the instance in Portainer that the script is interacting with. |
| `NETWORK_NAME` | The name of the network that the script is checking or adding to the container. |
| `SAVE_RESPONSE` | A boolean indicating whether the response from the Portainer API should be saved to a file. |
| `OUT_FILE_NAME` | The name of the file where the response from the Portainer API is saved if `SAVE_RESPONSE` is `True`. |