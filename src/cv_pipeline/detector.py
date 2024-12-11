from pathlib import Path
import torch
from ultralytics import YOLO
import cv2
import numpy as np
from matplotlib import pyplot as plt

class ObjectDetector:
    def __init__(self, model_path="models/yolov9c.pt"):
        """Initialize YOLOv9 detector."""
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(model_path)
        self.model.to(self.device)
        
    def detect(self, frame):
        """Detect objects in frame."""
        results = self.model(frame)
        detections = []
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = float(box.conf)
                cls = int(box.cls)
                detections.append({
                    'bbox': [x1, y1, x2, y2],
                    'confidence': conf,
                    'class': cls
                })
                
        return detections
    
if __name__ == "__main__" :
    detector = ObjectDetector()
    frame = cv2.imread("data/images/sample_1.jpeg")
    detections = detector.detect(frame)
    print(f'Detections : {detections}')
    # plot detections on frame for visualization
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        # convert to int
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # set name at the top of the rectangle 
        # cv2.putText(frame, str(det['class']), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    print('frame shape:', frame.shape)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.show()