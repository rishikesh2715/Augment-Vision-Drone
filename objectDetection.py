import cv2
from ultralytics import YOLO
import supervision as sv

def main():
        box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=1,
            text_scale=0.5,
        )

        model = YOLO('yolov8n.pt')

        for result in model.track(source="1", show=False, stream=True, classes=0):
            frame = result.orig_img
            detections = sv.Detections.from_yolov8(result)        

            if result.boxes.id is not None:
                detections.tracker_id = result.boxes.id.cpu().numpy() .astype(int)

            lables = [
                f"#{tracker_id}{class_id} {confidence:.2f}"
                for xyxy, confidence, class_id, tracker_id
                in detections
            ]
            frame = box_annotator.annotate(scene=frame, detections=detections, labels=lables)

            if detections.xyxy.any():
                [x1, y1, x2, y2] = detections.xyxy[0]
                               
                #Camera parameters
                focal_length = 730  # C920 webcam focal 
                drone_real_width = 0.41  # Tello width

                drone_pixel_width = x2 - x1
                distance = (drone_real_width * focal_length) / drone_pixel_width
                
                print(f"{distance:.2f} m")

            cv2.imshow("frame", frame)
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                    break


if __name__ == "__main__":
    main()
            
        
    
                    