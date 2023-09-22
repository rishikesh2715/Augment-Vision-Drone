import sys
import math
from telemetry import processSerialData
import time
import display_heading
import objectDetection
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.environ.get('CHS_PATH'))
import JY901S
import multiprocessing

class DroneState:
    def __init__(self, lat, lon, speed, altitude, heading, pitch, roll, yaw, sats, objectDistance, offsetAngle):
        self.lat = lat
        self.lon = lon
        self.speed = speed
        self.altitude = altitude
        self.heading = heading
        self.sats = sats
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        self.objectDistance = objectDistance
        self.offsetAngle = offsetAngle

class PilotState:
    def __init__(self, lat, lon, direction, altitude, objectDirection, objectDistance):
        self.lat = lat
        self.lon = lon
        self.direction = direction
        self.altitude = altitude
        self.objectDirection = objectDirection
        self.objectDistance = objectDistance

def haversine_distance_meters(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = R * c
    distance_m = distance_km * 1000  # Convert to meters
    return distance_m

def getVector(drone_latitude, drone_longitude, drone_altitude, drone_heading, drone_pitch, drone_roll, your_latitude, your_longitude, drone, pilot):
    print(drone_latitude)
    # GPS coordinates
    drone_latitude = 33.565325
    drone_longitude = -101.869024
    drone_altitude = 0
    drone_heading = 90

    your_latitude = 33.565371
    your_longitude = -101.868981


    north_south_diff = haversine_distance_meters(drone_latitude, drone_longitude, your_latitude, drone_longitude)
    east_west_diff = haversine_distance_meters(drone_latitude, drone_longitude, drone_latitude, your_longitude)

    # Adjust for direction (north/south and east/west)
    if drone_latitude < your_latitude:
        north_south_diff = -north_south_diff
    if drone_longitude < your_longitude:
        east_west_diff = -east_west_diff
    # Calculate position vector from your location to the drone
    v1 = (
        north_south_diff,
        east_west_diff,
        drone.altitude - pilot.altitude
    )
    
    # Calculate direction vector from the drone to the target object
    target_altitude = drone_altitude
    # drone.objectDistance = 10

    # Calculate the actual direction from the drone to the detected object
    # drone.offsetAngle = 15
    droneToObjectDirection = (drone_heading + drone.offsetAngle) % 360

    # Calculate direction vector from the drone to the target object
    v2 = (
        drone.objectDistance * math.cos(math.radians(drone_pitch)) * math.sin(math.radians(droneToObjectDirection)),
        drone.objectDistance * math.cos(math.radians(drone_pitch)) * math.cos(math.radians(droneToObjectDirection)),
        drone.objectDistance * math.sin(math.radians(drone_pitch))
    )



    # Calculate vector from your location to the target object
    v3 = (
    v1[0] + v2[0],
    v1[1] + v2[1],
    v1[2] + v2[2]
    )

    pilot.objectDirection = math.degrees(math.atan2(v3[1], v3[0]))
    pilot.objectDirection = (pilot.objectDirection + 360) % 360

    # add the offset angle from the drone camera to the pilot heading
    pilot.objectDirection += drone.offsetAngle
    pilot.objectDirection = (pilot.objectDirection + 360) % 360

    pilot.objectDistance = math.sqrt(v3[0]**2 + v3[1]**2 + v3[2]**2)

    # Print the vectors
    # print("Vector from your location to the drone (V1):", v1)
    # print("Vector from the drone to the target object (V2):", v2)
    # print("Vector from your location to the target object (V3):", v3)
    # print(f"{pilot.objectDistance:.2f} degrees")


def runGPSscript(pilot, q):
    JY901S.runScript(pilot, q)


drone = DroneState(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
pilot = PilotState(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

def getCompassDirection():
    global pilot
    # print (f"Direction: {pilot.direction}")
    return pilot.direction

if __name__ == "__main__":
    gpsQueue = multiprocessing.Queue()
    gpsProcess = multiprocessing.Process(target=runGPSscript, args=(pilot, gpsQueue,))
    gpsProcess.daemon = False # Daemon Process exit when the program does
    gpsProcess.start()

    objectDistance = multiprocessing.Value('f', 0.0)
    offsetAngle = multiprocessing.Value('f', 0.0)

    displayHeadingQueue = multiprocessing.Queue()
    displayHeadingProcess = multiprocessing.Process(target=display_heading.display_heading, args=(pilot, drone, displayHeadingQueue, objectDistance, offsetAngle ))
    displayHeadingProcess.daemon = False
    displayHeadingProcess.start()

    objectDetectionProcess = multiprocessing.Process(target=objectDetection.objectDetection, args=(objectDistance, offsetAngle,))
    objectDetectionProcess.start()

    # serialQueue = multiprocessing.Queue()
    # serialProcess = multiprocessing.Process(target=processSerialData, args=(drone,))
    # serialProcess.daemon = True
    # serialProcess.start()


    while True:
        if not gpsQueue.empty():
            pilot = gpsQueue.get()
        if not displayHeadingQueue.empty():
            drone, pilot = displayHeadingQueue.get()
        # if not serialQueue.empty():
        #     drone = serialQueue.get()
        drone.objectDistance = objectDistance.value
        drone.offsetAngle = offsetAngle.value
        print("Object Distance:", drone.objectDistance)
        getVector(drone.lat, drone.lon, drone.altitude, drone.heading, drone.pitch, drone.roll, pilot.lat, pilot.lon, drone, pilot)
        getCompassDirection()
        time.sleep(0.1)
