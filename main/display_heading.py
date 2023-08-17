import sys
import threading
import time
import cv2
import numpy as np

sys.path.append('main/WitStandardProtocol_JY901/Python/PythonWitProtocol/chs')
import main

def rotate_image(image, angle):
    center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return rotated_image

def overlay_transparent(background, overlay, x, y):
    h, w, _ = overlay.shape
    foreground = overlay[:, :, :3]
    
    alpha = overlay[:, :, 3] / 255.0
    for c in range(0, 3):
        background[y:y+h, x:x+w, c] = (1.0 - alpha) * background[y:y+h, x:x+w, c] + alpha * foreground[:, :, c]
    return background

def compass_direction(compass_image):
    while True:
        direction = main.getCompassDirection()
        if direction is not None:
            print("Compass Direction:", direction)
        else:
            print("Compass direction data is not available.")
        time.sleep(0.1)  # Adjust the sleep interval as needed

if __name__ == "__main__":
    # Initialize camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera.set(cv2.CAP_PROP_FPS, 30.0)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    target_width = 2560
    target_height = 1440

    # Load compass image with transparency
    compass_img = cv2.imread('compass_white.png', cv2.IMREAD_UNCHANGED)

    # Resize compass image 
    compass_img = cv2.resize(compass_img, (400, 400))  # Adjust size as needed

    # Start the compass direction thread
    gpsThread = threading.Thread(target=main.runGPSscript, args=(main.pilot,))
    gpsThread.daemon = True  # Daemon threads exit when the program does
    gpsThread.start()

    compass_thread = threading.Thread(target=compass_direction, args=(compass_img,))
    compass_thread.daemon = True
    compass_thread.start()

    font = cv2.FONT_HERSHEY_TRIPLEX  # font style
    font_scale = 1.5  # font size
    font_color = (255, 255, 255) # font color 
    font_thickness = 2 # font thickness

    while True:
        # Read the camera frames
        retval, im = camera.read()
        if not retval:
            break

        # Upscale the frame from 1080p to 1440p
        resized_frame = cv2.resize(im, (target_width, target_height))

        # Get the compass direction
        direction = main.getCompassDirection()

        if direction is not None:
            print("Compass Direction:", direction)

            # Rotate the compass image based on the direction angle
            rotated_compass = rotate_image(compass_img, direction)

            # Overlay the rotated compass image in the top-right corner
            overlayed_frame = overlay_transparent(resized_frame, rotated_compass, target_width - rotated_compass.shape[1], 0)

            # Display the heading value as text und
            heading_text = "Heading: {:.2f}".format(direction)
            text_size = cv2.getTextSize(heading_text, font, font_scale, font_thickness)[0]
            text_x = target_width - rotated_compass.shape[1] - 25  # X-axis--align text with PNG image
            text_y = rotated_compass.shape[0] + text_size[1] + 10  # Y-axis--align text with PNG image
            cv2.putText(overlayed_frame, heading_text, (text_x, text_y), font, font_scale, font_color, font_thickness)

        cv2.imshow("image", overlayed_frame)

        # Press 'ESC' for exiting video
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    camera.release()
    cv2.destroyAllWindows()
