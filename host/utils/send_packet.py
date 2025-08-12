import json
import requests

with open("host/config/client_wifi.json", "r") as client_wifi:
    config = json.load(client_wifi)

def send_packet(json_data):
    try:
        url = f"http://{config['host_ip']}{config['endpoint']}"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)
        print(response.status_code, response.text)
    except Exception as e:
        print(f"Error sending packet: {e}")
