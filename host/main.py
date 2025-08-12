import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import telemetry.f1_2020 as f1_2020
import utils.build_packet as build_packet
import utils.send_packet as send_packet

def main():    
    try:
        while True:
            data = f1_2020.run()
            if data:
                json_body = build_packet.create_json_packet(data)
                if json_body:
                    start_time = time.time()
                    send_packet.send_packet(json_body)
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"Packet sent in {elapsed:.2f} seconds")
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")

if __name__ == "__main__":
    main()