import cv2
from ultralytics import YOLO
import supervision as sv
import platform

def objectDetection(drone):
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5,
    )

    model = YOLO('yolov8n.pt')

    for result in model.track(source="2", show=False, stream=True, classes=0, verbose=False):
        frame = result.orig_img
        detections = sv.Detections.from_yolov8(result)        

        # print(detections)

        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy() .astype(int)

        if platform.system().lower() == 'linux':
            lables = [
                f"#{tracker_id}{class_id} {confidence:.2f}"
                for xyxy, mask, confidence, class_id, tracker_id
                in detections
            ]
        else:
            lables = [
                f"#{tracker_id}{class_id} {confidence:.2f}"
                for xyxy, confidence, class_id, tracker_id
                in detections
            ]    
        frame = box_annotator.annotate(scene=frame, detections=detections, labels=lables)

        if detections.xyxy.any():
            [x1, y1, x2, y2] = detections.xyxy[0]
                            
            #Camera parameters
            FOV = 160 # walknail avatar camera fov
            focal_length = 730  # drone cam focal // c920 = 730 
            Object_Real_Height = 1.8  # Average Human Height in meters
            # print (f"{x1, y1, x2, y2}")
            
            # calculating the heading offset from the center of the frame
            object_center_x = (x1 + x2) / 2
            frame_center_x = frame.shape[1] / 2
            offset_x = object_center_x - frame_center_x

            drone.offsetAngle = (offset_x/frame.shape[1]) * (FOV) # angle offset from center of frame
            # print(f"offset angle is {drone.offsetAngle:.2f} degrees")

            # calculating the distance to the object
            drone_pixel_height = y2 - y1
            drone.objectDistance = (Object_Real_Height * focal_length) / drone_pixel_height
            
            print(f"object distance is{drone.objectDistance:.2f} m")

        else:
            drone.objectDistance = 0

        cv2.imshow("frame", frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            break

    
    cv2.destroyAllWindows()

        
    
                    