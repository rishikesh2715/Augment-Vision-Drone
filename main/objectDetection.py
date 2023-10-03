from ultralytics import YOLO
import cv2
import platform
import time

def get_objects(results, frame, objectDistance, offsetAngle):
    detected_objects = []
    
    # Camera parameters
    FOV = 160  # walknail avatar camera fov
    focal_length = 730  # drone cam focal // c920 = 730 
    Object_Real_Height = 1.8  # Average Human Height in meters

    if not len(results):
        offsetAngle = 0
        objectDistance = 0
        # Append default object when no detections are available
        detected_objects.append({
            'bbox': None,
            'class_name': None,
            'confidence': 0,
            'class_id': None,
            'distance': 0,
            'offset': 0,
            'objectDistance': objectDistance,
            'offsetAngle': offsetAngle
        })
        return detected_objects

    for det in results:
        if len(det.boxes.xyxy) > 0:
            # Extract bounding boxes
            xyxy = det.boxes.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, xyxy)

            # Extract class name and confidence score
            class_id = int(det.boxes.cls[0])
            class_name = det.names[class_id]
            confidence = float(det.boxes.conf[0])

            # calculating the heading offset from the center of the frame
            object_center_x = (x1 + x2) / 2
            frame_center_x = frame.shape[1] / 2
            offset_x = object_center_x - frame_center_x

            offsetAngle.value = (offset_x/frame.shape[1]) * (FOV) # angle offset from center of frame
            

            # calculating the distance to the object
            drone_pixel_height = y2 - y1
            objectDistance.value = (Object_Real_Height * focal_length) / drone_pixel_height
            

            detected_objects.append({
                'bbox': (x1, y1, x2, y2),
                'class_name': class_name,
                'confidence': confidence,
                'class_id': class_id,
                'distance': objectDistance,
                'offset': offsetAngle
            })
    return detected_objects

def objectDetection(objectDistance, offsetAngle):
    try:
        print("Starting objectDetection function...")
        # Initialize camera
        if platform.system().lower() == 'linux':
            cap = cv2.VideoCapture(2)
            print("Camera initialized...")
        else:
            cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

        if not cap.isOpened():
            print("Error: Could not open camera 2.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
        model = YOLO('yolov8n.pt')

        while True:
            ret, frame = cap.read()

            # print('capped a frame')

            if not ret:
                print("Failed to grab frame")
                break

            results = model(frame)
            detected_objects = get_objects(results, frame, objectDistance, offsetAngle)

            if len(detected_objects) != 0:
                for obj in detected_objects:
                    # Access properties of each object:
                    bbox = obj['bbox']
                    class_name = obj['class_name']
                    confidence = obj['confidence']
                    class_id = obj['class_id']
                    distance = obj['distance']
                    
                    # For instance, you can draw bounding boxes using OpenCV
                    color = (0, 255, 0)  # green color for bounding boxes
                    cv2.rectangle(frame, bbox[0:2], bbox[2:4], color, 2)
                    label = f"{class_name} {distance.value:.2f}m"
                    cv2.putText(frame, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            cv2.imshow("YOLO Stream", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("q pressed, exiting...")
                break

        print("Releasing resources in objectDetection...")
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print("Exception in objectDetection:", e)
