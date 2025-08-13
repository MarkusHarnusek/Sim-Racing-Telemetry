# Data Packets

This document provides detailed information about the data packets used by the Sim-Racing-Telemetry application to communicate with host devices.

## Packet Overview

The packets do not directly contain telemetry data. Instead, they provide instructions for the host device on how its components should behave. This design minimizes heavy processing on the host device, saving space and enabling greater configuration flexibility.

## Example Packet Structure

Below is an example of a typical packet:

```json
{
    "id": 1,
    "gear": 2,
    "flag-values": {
        "R": 0,
        "G": 255,
        "B": 255
    },
    "rpm-values": [
        255,
        255,
        255,
        255,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]
}
```

### Explanation of Fields

- **id**: A unique identifier for the packet.
- **gear**: Represents the current gear of the vehicle.
- **flag-values**: Contains RGB values for flags, where:
  - `R`: Red component.
  - `G`: Green component.
  - `B`: Blue component.
- **rpm-values**: An array representing RPM values for different segments, useful for visualizing engine performance or other metrics.

This structure ensures efficient communication and processing, making it suitable for real-time applications in sim racing telemetry.