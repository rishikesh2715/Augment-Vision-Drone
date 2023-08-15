# import sys

# sys.path.append('D:\projectLab5\Augment-Vision-Drone\main\WitStandardProtocol_JY901\Python\PythonWitProtocol\chs')
# import JY901S

# def compass_direction():
#     direction = JY901S.pilot.get('direction')
#     if direction is not None:
#         print("Compass Direction:", direction)
#     else:
#         print("Compass direction data is not available.")

# if __name__ == "__main__":
#     compass_direction()



import cv2

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

camera.set(cv2.CAP_PROP_FPS, 30.0)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = camera.get(cv2.CAP_PROP_FPS)

print (width, height, fps) # fps is printing 0s?

while (1):
    retval, im = camera.read()
    cv2.imshow("image", im)

    k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

camera.release()
cv2.destroyAllWindows()
