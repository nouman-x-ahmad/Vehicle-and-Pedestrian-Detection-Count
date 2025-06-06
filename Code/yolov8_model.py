from ultralytics import YOLO

# COCO class mapping including bicycle→motorcycle
COCO_CLASSES = {
    0: "pedestrian",
    1: "motorcycle",   # bicycle also treated as motorcycle
    2: "car",
    3: "motorcycle",
    5: "bus",          # will normalize to "truck"
    7: "truck"
}

class VehicleDetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.3, moto_threshold=0.2):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        # for class 1 & 3 (motorcycle), use a lower threshold
        self.moto_threshold = moto_threshold

    def detect_vehicles(self, frame):
        results = self.model(frame, verbose=False)[0]
        detections = []

        if results.boxes is None or results.boxes.shape[0] == 0:
            return detections

        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            # choose threshold per class
            thr = self.moto_threshold if cls_id in (1,3) else self.conf_threshold

            if conf < thr:
                continue

            # initial label from mapping or rest
            label = COCO_CLASSES.get(cls_id, "rest")
            if label == "bus":
                label = "truck"

            w, h = x2 - x1, y2 - y1

            # if YOLO thought it was pedestrian but box is wide → likely a bike
            if label == "pedestrian" and w / (h+1e-6) > 0.75:
                old = label
                label = "motorcycle"
                print(f"Re‑labeled from {old}→{label} by aspect‑ratio ({w:.1f}/{h:.1f})")

            detections.append(([x1, y1, w, h], conf, label))
            print(f"Detected: {label} ({conf:.2f})  box_w/h={w/h:.2f}")

        return detections
