# Auto-add-network-to-docker-container
This Python script interacts with the Portainer API to manage Docker containers and networks. Here's a step-by-step breakdown of what it does:

1. **Setup**: It first sets up the Portainer URL, username, and API key, and defines the container and network details using the environment variables `PORTAINER_URL`, `PORTAINER_USERNAME`, `PORTAINER_PASSWORD`, `CONTAINER_NAME`, and `NETWORK_NAME`. `SAVE_RESPONSE` set to `True` you can save the response from the GET request to a JSON file.

2. **Get Containers**: It sends a GET request to the Portainer API to retrieve a list of all Docker containers. Set the `INSTANCE_ID` to define which docker environment to use (This can be found in the URL and must be a number, in most cases `1`). The response is converted to a list of dictionaries, where each dictionary represents a container.

3. **Find Container**: It filters the list of containers to find the one with the name specified in `CONTAINER_NAME`. It then retrieves the network settings for this container.

4. **Check Network**: It checks if the container is already connected to the network specified in `NETWORK_NAME`. If it's not, it proceeds to the next step.

5. **Connect to Network**: It sends a POST request to the Portainer API to connect the container to the network. It prints the status code and text of the response.

6. **Save Response**: If the `SAVE_RESPONSE` variable is set to `True`, it writes the response from the GET request (the list of all containers) to a JSON file named 'container_data.json' if not overwritten by `OUT_FILE_NAME`. If `SAVE_RESPONSE` is `False`, it skips this step.

# Usage

1. Set up all environment variables. Remember to set PUID and PGID for security reasons.
