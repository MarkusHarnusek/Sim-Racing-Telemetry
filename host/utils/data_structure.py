# This file contains the data structure for telemetry data

def initialize_data():
    """
    Initializes the telemetry data structure.

    Returns:
        dict: A dictionary containing default values for telemetry data.

        Keys:
            player_car_index (int): Index of the player's car.
            rpm (int): Engine RPM.
            speed (int): Car speed in km/h.
            gear (int): Current gear (-1 for reverse, 0 for neutral, 1-8 for forward gears).
            car_position (int): Position of the car on the track.
            pit-limiter (int): Status of the pit limiter (0: off, 1: on).
            drs (bool): Drag Reduction System status (True: active, False: inactive).
            drs_allowed (bool): Whether DRS is allowed (True: allowed, False: not allowed).
            flag (int): Current flag status (0: no flag, 1: yellow flag, etc.).
            safety_car (int): Safety car status (0: no safety car, 1: virtual safety car, 2: full safety car).
    """
    return {
        "player_car_index": 0,  # Default player car index
        "rpm": 0,              # Default engine RPM
        "speed": 0,            # Default car speed
        "gear": 0,             # Default gear
        "car_position": 0,     # Default car position
        "pit-limiter": 0,      # Default pit limiter status
        "drs": False,          # Default DRS status
        "drs_allowed": False,  # Default DRS allowance status
        "flag": 0,             # Default flag status
        "safety_car": 0        # Default safety car status
    }