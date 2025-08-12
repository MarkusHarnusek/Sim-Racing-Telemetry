import json

# Function to create a JSON packet from telemetry data
def create_json_packet(data, file_path="telemetry_packet.json"):
    try:
        #Convert the data object into a JSON string
        json_data = json.dumps(data, indent=4)
        
        # Write the JSON string to a file
        with open(file_path, 'w') as json_file:
            json_file.write(json_data)
    except Exception as e:
        print(f"Error creating JSON packet: {e}")
        
# Example data object for testing
if __name__ == "__main__":
    example_data = {
        "player_car_index": 19,
        "rpm": 10763,
        "speed": 203,
        "gear": 5,
        "car_position": 15,
        "pit_limiter": 0,
        "drs": False,
        "drs_allowed": False,
        "flag": 3,
        "safety_car": 0
    }

    # Create a JSON file from the example data
    create_json_packet(example_data)