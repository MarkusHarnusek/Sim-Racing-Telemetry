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
    "flag": 0,
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
    ],
    "event": 0
}
```

### Explanation of Fields

- **id**: A unique identifier for the packet.
- **gear**: Represents the current gear of the vehicle. Special values include:
  - `10`: Neutral gear.
  - `11`: Reverse gear.
- **flag**: Represents the race condition or warning status. Possible values include:
  - `0`: None - No flag is active; normal racing conditions.
  - `1`: Green Flag - The track is clear, and normal racing conditions apply.
  - `2`: Blue Flag - A faster car is approaching; the driver must let them pass.
  - `3`: Yellow Flag - Caution due to an incident on the track; drivers must slow down and avoid overtaking.
  - `4`: Red Flag - The session has been stopped due to severe conditions or incidents.
- **rpm-values**: An array representing RPM values for different segments, useful for visualizing engine performance or other metrics.
- **event**: This property tells the client about game events, some values are:
  - `0`: None - No event has happend
  - `1`: Redline - The RPM value of the vehicle has exceeded the redline value

This structure ensures efficient communication and processing, making it suitable for real-time applications in sim racing telemetry.