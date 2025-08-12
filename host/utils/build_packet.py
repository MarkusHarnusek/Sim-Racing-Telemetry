import json

# Function to create a JSON packet from telemetry data
def create_json_packet(data, file_path="telemetry_packet.json"):
    try:
        #Convert the data object into a JSON string
        json_data = json.dumps(data, indent=4)
        
        # Write the JSON string to a file
        with open(file_path, 'w') as json_file:
            json_file.write(json_data)
            return json_data
    except Exception as e:
        print(f"Error creating JSON packet: {e}")
        return None