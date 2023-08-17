import sys
import threading
import time
sys.path.append('main/WitStandardProtocol_JY901/Python/PythonWitProtocol/chs')
import main

def compass_direction():
    direction = main.getCompassDirection()
    if direction is not None:
        print("Compass Direction:", direction)
    else:
        print("Compass direction data is not available.")

if __name__ == "__main__":
    gpsThread = threading.Thread(target=main.runGPSscript, args=(main.pilot,))
    gpsThread.daemon = True # Daemon threads exit when the program does
    gpsThread.start()
    time.sleep(1)
    compass_direction()


import cv2
import numpy as np

compass_img = cv2.imread('compass.png', cv2.IMREAD_UNCHANGED)

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

camera.set(cv2.CAP_PROP_FPS, 30.0)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

target_width = 2560    
target_height = 1440

while (1):
    # read the camera frames
    retval, im = camera.read()
    if not retval: break

    #upscale the frame from 1080p to 1440p
    resized_frame = cv2.resize(im, (target_width, target_height)) 
    cv2.imshow("image", resized_frame)

    # Press 'ESC' for exiting video
    k = cv2.waitKey(1) & 0xff 
    if k == 27:
        break

camera.release()
cv2.destroyAllWindows()
