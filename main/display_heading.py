import sys
import threading
import time
import cv2
import numpy as np

target_width = 1920
target_height = 1080

# Calculate the position of the triangle based on direction and distance
# triangle_heading = 180  # Use the current direction as the heading
triangle_distance = 10  # 10 meters, adjust as needed

camFOVangle = 60

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

def compass_direction(compass_image, pilot):
    while True:
        direction = pilot.direction
        if direction is not None:
            pass
            #print("Compass Direction:", direction)
        else:
            print("Compass direction data is not available.")
        time.sleep(0.1)  # Adjust the sleep interval as needed

def drawTriangle(pilot, direction, resized_frame):

    direction_difference = pilot.objectDirection - direction
    if direction_difference <= 0:
        direction_difference += 360
    if direction_difference >= 330:
        direction_difference -= 360
    
    x_triangle = int(target_width / 2 + direction_difference / (camFOVangle/2) * target_width / 2)
    y_triangle = target_height // 2

    # Draw the triangle at the calculated position
    triangle_size = int(target_height * (2 / pilot.objectDistance))  # Adjust size based on distance
    triangle_color = (0, 255, 0)  # Green color
    cv2.drawMarker(resized_frame, (x_triangle, y_triangle), triangle_color, markerType=cv2.MARKER_TRIANGLE_UP, markerSize=triangle_size)

def display_heading(pilot):
    # Initialize camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FPS, 30.0)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Load compass image with transparency
    compass_img = cv2.imread('compass_white.png', cv2.IMREAD_UNCHANGED)

    # Resize compass image 
    compass_img = cv2.resize(compass_img, (400, 400))  # Adjust size as needed

    compass_thread = threading.Thread(target=compass_direction, args=(compass_img,pilot,))
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
        direction = pilot.direction

        if direction is not None:
            # print("Compass Direction:", direction)

            # Calculate the angle difference between north (0 degrees) and current direction
            angle_difference = abs(direction)

            # Convert angle to radians
            triangle_heading_rad = np.radians(pilot.objectDirection)

            # Calculate the change in x and y based on heading and distance
            delta_x = pilot.objectDistance * np.sin(triangle_heading_rad)
            delta_y = -pilot.objectDistance * np.cos(triangle_heading_rad)

            # Calculate the position of the triangle relative to the center of the screen
            x_90_degrees = int(target_width / 2 + delta_x)
            y_90_degrees = int(target_height / 2 + delta_y)

            # Calculate the angle limits based on camera field of view
            angle_limit_left = (pilot.objectDirection - camFOVangle / 2) % 360
            angle_limit_right = (pilot.objectDirection + camFOVangle / 2) % 360


            if angle_limit_left <= angle_limit_right:
                if angle_limit_left <= direction <= angle_limit_right:
                    drawTriangle(pilot, direction, resized_frame)

            else:
                if direction >= angle_limit_left or direction <= angle_limit_right:
                    drawTriangle(pilot, direction, resized_frame)

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
