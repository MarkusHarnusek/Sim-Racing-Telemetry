import sys
import os
import time

# Add the parent directory to the system path to allow imports from sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import telemetry data processing module for F1 2020
import telemetry.f1_2020 as f1_2020
# Import utility module for building packets
import utils.build_packet as build_packet
# Import utility module for sending packets
import utils.send_packet as send_packet

def main():
    """
    Main function to continuously fetch telemetry data, build packets, and send them.

    The function runs in an infinite loop until interrupted by the user.
    It fetches telemetry data using the `f1_2020.run()` function, builds a JSON packet
    using `build_packet.build_packet()`, and sends the packet using `send_packet.send_packet()`.
    The time taken to send each packet is printed to the console.
    """
    try:
        while True:
            # Fetch telemetry data from F1 2020
            data = f1_2020.run()
            if data:
                # Build a JSON packet from the telemetry data
                json_body = build_packet.build_packet(data)
                if json_body:
                    # Measure the time taken to send the packet
                    start_time = time.time()
                    send_packet.send_packet(json_body)
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"Packet sent in {elapsed:.2f} seconds")
    except KeyboardInterrupt:
        # Handle user interruption gracefully
        print("\nScript interrupted by user.")

if __name__ == "__main__":
    # Entry point of the script
    main()