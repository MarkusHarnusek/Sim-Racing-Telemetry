import telemetry.f1_2020 as f1_2020
import utils.build_packet as build_packet
import utils.send_packet as send_packet

import utils.data_structure as data_structure # DEBUG

def main():
    try:
        data = data_structure.initialize_data()  # DEBUG
        if data:
            json_body = build_packet.create_json_packet(data)
            if json_body:
                send_packet.send_packet(json_body)
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")

if __name__ == "__main__":
    main()