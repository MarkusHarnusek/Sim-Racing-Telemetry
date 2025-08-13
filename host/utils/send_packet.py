import json
import requests

# Load client WiFi configuration from the configuration file
with open("host/config/client_wifi.json", "r") as client_wifi:
    config = json.load(client_wifi)

def send_packet(json_data):
    """
    Sends a JSON packet to a specified endpoint using an HTTP POST request.

    Args:
        json_data (str): JSON string containing telemetry data to be sent.

    Returns:
        None

    Prints:
        HTTP response status code and response text if the request is successful.
        Error message if an exception occurs during the process.
    """
    try:
        # Construct the URL using the host IP and endpoint from the configuration
        url = f"http://{config['host_ip']}{config['endpoint']}"
        
        # Set the headers for the HTTP request
        headers = {'Content-Type': 'application/json'}
        
        # Send the HTTP POST request with the JSON data
        response = requests.post(url, data=json_data, headers=headers)
        
        # Print the response status code and text for debugging
        print(response.status_code, response.text)
    except Exception as e:
        # Print an error message if an exception occurs
        print(f"Error sending packet: {e}")