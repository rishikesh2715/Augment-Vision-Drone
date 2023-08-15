import sys

sys.path.append('D:\projectLab5\Augment-Vision-Drone\main\WitStandardProtocol_JY901\Python\PythonWitProtocol\chs')
import JY901S

def compass_direction():
    direction = JY901S.pilot.get('direction')
    if direction is not None:
        print("Compass Direction:", direction)
    else:
        print("Compass direction data is not available.")

if __name__ == "__main__":
    compass_direction()


