import cv2

def main():
    # Start capture from the first camera (usually the built-in webcam)
    cap1 = cv2.VideoCapture(1)

    # Start capture from the second camera
    cap2 = cv2.VideoCapture(0)

    if not cap1.isOpened() or not cap2.isOpened():
        print("Error: Couldn't open one or both cameras.")
        return

    while True:
        # Capture frame-by-frame for the first camera
        ret1, frame1 = cap1.read()

        # Capture frame-by-frame for the second camera
        ret2, frame2 = cap2.read()

        # If frames were captured, display them
        if ret1:
            cv2.imshow('Camera 1', frame1)

        if ret2:
            cv2.imshow('Camera 2', frame2)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video captures and close windows
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
