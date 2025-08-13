import socket
import json
from f1_2020_telemetry.packets import unpack_udp_packet
from host.utils.data_structure import initialize_data

# Load UDP settings from the configuration file
with open("host/config/udp_settings.json", "r") as udp_settings:
    config = json.load(udp_settings)

def run():
    """
    Main function to collect telemetry data from F1 2020 game via UDP.

    This function sets up a UDP socket, listens for incoming telemetry packets,
    processes the packets based on their type, and extracts relevant data.

    Returns:
        dict: A dictionary containing processed telemetry data.
    """

    # UDP setup
    UDP_IP = config["f1_2020"]["ip"]  # IP address to bind the socket
    UDP_PORT = config["f1_2020"]["port"]  # Port to bind the socket
    TIMEOUT = config["f1_2020"]["timeout"]  # Timeout for the socket

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(TIMEOUT)

    # Mapping for DRS (Drag Reduction System) status
    drs_map = { 0: False, 1: True }

    # Initialize the data structure to store telemetry data
    data = initialize_data()

    while True:
        try:
            # Receive data from the socket
            packet_data, addr = sock.recvfrom(2048)
            packet = unpack_udp_packet(packet_data)
            packetId = packet.header.packetId
    
            # Check if the packet is valid
            if packet:
                if packetId == 6:  # 6 corresponds to car telemetry packets
                    telemetry = packet.carTelemetryData[packet.header.playerCarIndex]
                    # Extract telemetry data such as RPM, speed, gear, and DRS status
                    data["rpm"] = telemetry.engineRPM if hasattr(telemetry, 'engineRPM') and telemetry.engineRPM is not None else 0
                    data["speed"] = int(telemetry.speed) if hasattr(telemetry, 'speed') and telemetry.speed is not None else 0
                    data["gear"] = telemetry.gear if hasattr(telemetry, 'gear') and telemetry.gear is not None else 0
                    data["drs"] = drs_map.get(telemetry.drs, False) if hasattr(telemetry, 'drs') and telemetry.drs is not None else False
                elif packetId == 2: # 2 corresponds to lap data packets
                    lap = packet.lapData[packet.header.playerCarIndex]
                    # Extract lap data such as car position and pit limiter status
                    data["car_position"] = lap.carPosition if hasattr(lap, 'carPosition') and lap.carPosition is not None else 0
                    data["pit-limiter"] = lap.pitStatus if hasattr(lap, 'pitStatus') and lap.pitStatus is not None else 0
                elif packetId == 1:  # 1 corresponds to marshal status packets
                    # Extract marshal status data such as player car index and safety car status
                    data["player_car_index"] = packet.header.playerCarIndex if hasattr(packet.header, 'playerCarIndex') and packet.header.playerCarIndex is not None else 0
                    data["safety_car"] = packet.safetyCarStatus if hasattr(packet, 'safetyCarStatus') and packet.safetyCarStatus is not None else 0
                elif packetId == 7:  # 7 corresponds to car status
                    # Extract car status data such as FIA flags and DRS allowance
                    fia_flags = [car.vehicleFiaFlags for car in packet.carStatusData if car.vehicleFiaFlags != 0]
                    data["flag"] = fia_flags[0] if fia_flags else 0
                    data["drs_allowed"] = drs_map.get(packet.drsAllowed, False) if hasattr(packet, 'drsAllowed') and packet.drsAllowed is not None else False

                    print(data) # DEBUG

                    return data # Return the data after processing
        except socket.timeout:
            # Handle socket timeout
            print("Socket timed out, waiting for data...")

if __name__ == "__main__":
    try:
        while True:
            run()        
    except KeyboardInterrupt:
        # Handle keyboard interrupt to stop telemetry data collection
        print("Telemetry data collection stopped.")