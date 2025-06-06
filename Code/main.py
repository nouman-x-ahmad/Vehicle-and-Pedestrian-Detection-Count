import tkinter as tk
from gui import VideoSelectorApp
import cv2
import json
from yolov8_model import VehicleDetector
from tracker import Tracker
from utils import estimate_speed, draw_ui

if __name__ == "__main__":
    # --- GUI for video and ROI selection ---
    root = tk.Tk()
    app = VideoSelectorApp(root)
    root.mainloop()

    # --- Prepare detection, tracking, speed estimation ---
    detector = VehicleDetector()
    tracker = Tracker()
    cap = app.cap
    fps = cap.get(cv2.CAP_PROP_FPS)
    roi = app.roi
    object_data = {}
    scale_ft_per_pixel = (1 / ((8 * 20) ** 0.5))

    # --- Process video frames ---
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Crop to ROI
        x1, y1, x2, y2 = roi
        roi_frame = frame[y1:y2, x1:x2]

        # Detection and tracking
        detections = detector.detect_vehicles(roi_frame)
        tracked_objects = tracker.update_tracks(detections, roi_frame)

        # Draw boxes, estimate speed
        for obj in tracked_objects:
            if not obj.is_confirmed():
                continue
            track_id = obj.track_id
            bbox = obj.to_tlbr()
            cx, cy = int((bbox[0] + bbox[2]) / 2), int((bbox[1] + bbox[3]) / 2)

            if track_id not in object_data:
                object_data[track_id] = {'positions': [(cx, cy)], 'speed': 0}
            else:
                positions = object_data[track_id]['positions']
                positions.append((cx, cy))
                if len(positions) >= 2:
                    d_pixels = ((positions[-1][0] - positions[-2][0]) ** 2 + (positions[-1][1] - positions[-2][1]) ** 2) ** 0.5
                    d_ft = d_pixels * scale_ft_per_pixel
                    speed_kmph = estimate_speed(d_ft, 1 / fps)
                    object_data[track_id]['speed'] = speed_kmph

            speed = object_data[track_id]['speed']
            color = (0, 0, 255) if speed > 30 else (0, 255, 0)
            cv2.rectangle(roi_frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.putText(roi_frame, f"{speed:.1f} km/h", (int(bbox[0]), int(bbox[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Draw counts UI
        counts = tracker.get_counts()
        draw_ui(roi_frame, counts)
        frame[y1:y2, x1:x2] = roi_frame

        cv2.imshow("Vehicle Counter", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # --- Accuracy Measurement (console input) ---
    print("\n=== Accuracy Measurement ===")
    gt_counts = {}
    for cls in counts:
        while True:
            try:
                val = int(input(f"Enter ground truth count for {cls}: "))
                gt_counts[cls] = val
                break
            except ValueError:
                print("Please enter an integer.")

    def compute_accuracy(pred, gt):
        if gt == 0:
            return 100.0 if pred == 0 else 0.0
        return max(0.0, (1 - abs(pred - gt) / gt) * 100)

    print("\nResults:")
    for cls, pred in counts.items():
        gt = gt_counts.get(cls, 0)
        acc = compute_accuracy(pred, gt)
        print(f"{cls.title():<12} Predicted: {pred:<3} GroundTruth: {gt:<3} Accuracy: {acc:.1f}%")

    # Save accuracy results
    results = {cls: {'predicted': counts[cls], 'ground_truth': gt_counts[cls],
                     'accuracy_pct': compute_accuracy(counts[cls], gt_counts[cls])} for cls in counts}
    with open('accuracy_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nAccuracy results saved to accuracy_results.json")
