import json

with open("host/config/rpm_config.json", "r") as config_file:
    config = json.load(config_file)

id = 0

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
    
def build_packet(data):
    try:
        # Default return packet
        return_data = {
            "id": id,
            "gear": data["gear"],
            "flag" : data["flag"],
            "rpm-values": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "event" : 0
        }
        
        # Check for neutral and reverse gear to change value
       
        if data["gear"] == 0:
            return_data["gear"] = 10
        elif data["gear"] == -1:
            return_data["gear"] = 11
            
        # Validate flag data
        
        if data["flag"] == -1:
            return_data["flag"] = 1
            
        # Send yellow flag event in case of (Virtual) Safety Car

        if data['safety_car'] != 0:
            return_data["flag"] = 2

        # Convert and manage rpm data
        
        mode = config['mode']
        min_rpm = config['min_rpm']
        redline = config['redline']
        
        # Set rpm event to 1 if rpm exceeds redline
        if data["rpm"] > redline:
            return_data["rpm-event"] = 1
        else:
            return_data["rpm-event"] = 0
        
        rpmJ = (( config["redline"] - config["min_rpm"] ) / 12)
        
        if mode == "normal":
            for i in range(12):
                if data["rpm"] > (min_rpm + i * ( ( config["redline"] - config["min_rpm"] ) / 12) ):
                    return_data["rpm-values"][i] = 255          
        elif mode == "skip":
            for i in range(8):
                if data["rpm"] > (min_rpm + i * ( ( config["redline"] - config["min_rpm"] ) / 8) ):
                    return_data["rpm-values"][i + 4] = 255
        elif mode == "segment":
            for i in range(3):
                if data["rpm"] > (min_rpm + i * ( ( config["redline"] - config["min_rpm"] ) / 3) ):
                    for j in range(4):
                        return_data["rpm-values"][i * 4 + j] = 255        
        # Increment the id of the next packet
        id += 1

        # Return the json formatted data packet
        return create_json_packet(return_data)

    except Exception as e:
        return None