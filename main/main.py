import math
from telemetry import processSerialData
import time
import threading

class DroneState:
    def __init__(self, lat, lon, speed, altitude, heading, pitch, roll, yaw, sats):
        self.lat = lat
        self.lon = lon
        self.speed = speed
        self.altitude = altitude
        self.heading = heading
        self.sats = sats
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw

drone = DroneState(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

serialThread = threading.Thread(target=processSerialData, args=(drone,))
serialThread.start()


def getVector(drone_latitude, drone_longitude, drone_altitude, drone_heading, drone_pitch, drone_roll):
    print(drone_latitude)
    # GPS coordinates
    your_latitude = 33.6018033
    your_longitude = -101.9247864
    your_altitude = 0

    # Conversion constants
    feet_to_meters = 0.3048

    # Calculate position vector from your location to the drone
    v1 = (
        drone_latitude - your_latitude,
        drone_longitude - your_longitude,
        drone_altitude - your_altitude
    )

    # Calculate direction vector from the drone to the target object
    target_height_feet = 6.0
    target_height_meters = target_height_feet * feet_to_meters
    target_altitude = drone_altitude + target_height_meters
    v2 = (
        math.cos(math.radians(drone_pitch)) * math.cos(math.radians(drone_heading)),
        math.cos(math.radians(drone_pitch)) * math.sin(math.radians(drone_heading)),
        math.sin(math.radians(drone_pitch))
    )

    # Calculate target object position vector
    v3 = (
        drone_latitude - your_latitude,
        drone_longitude - your_longitude,
        target_altitude - your_altitude
    )

    # Calculate vector from your location to the target object
    v4 = (
        v2[0] - v1[0],
        v2[1] - v1[1],
        v2[2] - v1[2]
    )

    # Print the vectors
    print("Vector from your location to the drone (V1):", v1)
    print("Vector from the drone to the target object (V2):", v2)
    print("Vector from your location to the target object (V4):", v4)

while True:
    time.sleep(2)
    getVector(drone.lat, drone.lon, drone.altitude, drone.heading, drone.pitch, drone.roll)
