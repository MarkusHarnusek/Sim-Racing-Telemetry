import json

# Load RPM configuration from the configuration file
with open("host/config/rpm_config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize packet ID
id = 0

# Function to create a JSON packet from telemetry data
def create_json_packet(data, file_path="telemetry_packet.json"):
    """
    Converts telemetry data into a JSON packet and writes it to a file.

    Args:
        data (dict): Telemetry data to be converted into JSON.
        file_path (str): Path to save the JSON packet file.

    Returns:
        str: JSON string representation of the telemetry data.
        None: If an error occurs during the process.
    """
    try:
        # Convert the data object into a JSON string
        json_data = json.dumps(data, indent=4)
        
        # Write the JSON string to a file
        with open(file_path, 'w') as json_file:
            json_file.write(json_data)
            return json_data
    except Exception as e:
        print(f"Error creating JSON packet: {e}")
        return None

# Function to build a telemetry data packet
def build_packet(data):
    """
    Builds a telemetry data packet based on the input data and configuration.

    Args:
        data (dict): Telemetry data containing gear, flag, rpm, and safety car status.

    Returns:
        str: JSON string representation of the telemetry data packet.
        None: If an error occurs during the process.
    """
    try:
        # Default return packet structure
        return_data = {
            "id": id,  # Packet ID
            "gear": data["gear"],  # Current gear
            "flag": data["flag"],  # Current flag status
            "rpm-values": [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ],  # RPM values for visualization
            "event": 0  # Event status
        }
        
        # Check for neutral and reverse gear to change value
        if data["gear"] == 0:
            return_data["gear"] = 10  # Neutral gear
        elif data["gear"] == -1:
            return_data["gear"] = 11  # Reverse gear
            
        # Validate flag data
        if data["flag"] == -1:
            return_data["flag"] = 1  # Default flag value
            
        # Send yellow flag event in case of (Virtual) Safety Car
        if data['safety_car'] != 0:
            return_data["flag"] = 2  # Yellow flag for safety car

        # Convert and manage RPM data
        mode = config['mode']  # RPM mode from configuration
        min_rpm = config['min_rpm']  # Minimum RPM value
        redline = config['redline']  # Redline RPM value
        
        # Set RPM event to 1 if RPM exceeds redline
        if data["rpm"] > redline:
            return_data["rpm-event"] = 1
        else:
            return_data["rpm-event"] = 0
        
        # Calculate RPM segments
        rpmJ = ((config["redline"] - config["min_rpm"]) / 12)
        
        # Populate RPM values based on mode
        if mode == "normal":
            for i in range(12):
                if data["rpm"] > (min_rpm + i * rpmJ):
                    return_data["rpm-values"][i] = 255          
        elif mode == "skip":
            for i in range(8):
                if data["rpm"] > (min_rpm + i * ((config["redline"] - config["min_rpm"]) / 8)):
                    return_data["rpm-values"][i + 4] = 255
        elif mode == "segment":
            for i in range(3):
                if data["rpm"] > (min_rpm + i * ((config["redline"] - config["min_rpm"]) / 3)):
                    for j in range(4):
                        return_data["rpm-values"][i * 4 + j] = 255        
        
        # Increment the ID for the next packet
        id += 1

        # Return the JSON formatted data packet
        return create_json_packet(return_data)

    except Exception as e:
        print(f"Error building packet: {e}")
        return None