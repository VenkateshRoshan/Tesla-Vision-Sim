from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2
from matplotlib import pyplot as plt
from detector import ObjectDetector

class ObjectTracker:
    def __init__(self):
        """Initialize DeepSORT tracker."""
        self.tracker = DeepSort(
            max_age=30,
            n_init=3,
            max_cosine_distance=0.3
        )
        
    def update(self, detections, frame):
        """Update tracks with new detections."""
        detection_list = []
        for det in detections:
            bbox = det['bbox']
            # Convert tensors to CPU and then to numpy or plain Python types
            bbox = [float(b.cpu()) for b in bbox]
            conf = float(det['confidence'])  # Ensure confidence is a float
            if conf < 0.5:
                continue
            cls = int(det['class'])  # Ensure class is an integer
            detection_list.append(([bbox[0], bbox[1], 
                                    bbox[2] - bbox[0], 
                                    bbox[3] - bbox[1]], 
                                   conf, cls))
        
        tracks = self.tracker.update_tracks(detection_list, frame=frame)
        return tracks

if __name__ == "__main__":
    # Initialize Object Tracker
    tracker = ObjectTracker()
    # Initialize Object Detector
    detector = ObjectDetector()
    
    # Open video file or camera stream
    video_path = "data/videos/sample_1.mp4"
    cap = cv2.VideoCapture(video_path)
    
    # Check if video is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or unable to read the frame.")
            break
        
        # resize the frame to 640, 480
        frame = cv2.resize(frame, (640, 480))

        # Perform object detection
        detections = detector.detect(frame)
        
        # Update tracker with detections
        tracks = tracker.update(detections, frame)
        
        # Iterate through the tracks and visualize them
        for track in tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue  # Skip unconfirmed or outdated tracks

            # Get bounding box coordinates
            x1, y1, x2, y2 = track.to_ltrb()  # Convert track to bounding box in LTRB format
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to integers

            # Draw the bounding box on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Optionally, display the track ID
            track_id = track.track_id
            cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # print(f'Track ID: {track_id}, Class: {track["class"]}, Confidence: {track["confidence"]}')

        # Display the frame
        cv2.imshow("Object Tracking", frame)

        # Press 'q' to exit the video early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release video capture object and close display window
    cap.release()
    cv2.destroyAllWindows()
