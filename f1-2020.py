import socket
from f1_2020_telemetry.packets import unpack_udp_packet

# UDP setup
UDP_IP = "127.0.0.1"
UDP_PORT = 20777

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(1.0)

# drs mapping
drs_map = { 0: False, 1: True }

# data packet structure
data = {
    "player_car_index": 0,
    "rpm": 0,
    "speed": 0,
    "gear": 0,
    "car_position": 0,
    "pit-limiter": 0,
    "drs": False,
    "drs_allowed": False,
    "flag": 0,
    "safety_car": 0
}

try:
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
                    data["rpm"] = telemetry.engineRPM if hasattr(telemetry, 'engineRPM') and telemetry.engineRPM is not None else 0
                    data["speed"] = int(telemetry.speed) if hasattr(telemetry, 'speed') and telemetry.speed is not None else 0
                    data["gear"] = telemetry.gear if hasattr(telemetry, 'gear') and telemetry.gear is not None else 0
                    data["drs"] = drs_map.get(telemetry.drs, False) if hasattr(telemetry, 'drs') and telemetry.drs is not None else False
                elif packetId == 2: # 2 corresponds to lap data packets
                    lap = packet.lapData[packet.header.playerCarIndex]
                    data["car_position"] = lap.carPosition if hasattr(lap, 'carPosition') and lap.carPosition is not None else 0
                    data["pit-limiter"] = lap.pitStatus if hasattr(lap, 'pitStatus') and lap.pitStatus is not None else 0
                elif packetId == 1:  # 1 corresponds to marshal status packets
                    data["player_car_index"] = packet.header.playerCarIndex if hasattr(packet.header, 'playerCarIndex') and packet.header.playerCarIndex is not None else 0
                    data["safety_car"] = packet.safetyCarStatus if hasattr(packet, 'safetyCarStatus') and packet.safetyCarStatus is not None else 0
                elif packetId == 7:  # 7 corresponds to car status
                    fia_flags = [car.vehicleFiaFlags for car in packet.carStatusData if car.vehicleFiaFlags != 0]
                    data["flag"] = fia_flags[0] if fia_flags else 0
                    data["drs_allowed"] = drs_map.get(packet.drsAllowed, False) if hasattr(packet, 'drsAllowed') and packet.drsAllowed is not None else False

                print(data)
        except socket.timeout:
            print("Socket timed out, waiting for data...")
except KeyboardInterrupt:
    print("\nScript interrupted by user.")
finally:
    sock.close()