

# 🚦 Vehicle & Pedestrian Detection System
[![Python 3.10](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/Deep_Learning-YOLOv8-red)](https://ultralytics.com/yolov8)
```markdown
> Real-time detection, tracking, counting, and speed estimation for traffic analysis
> Automated traffic analysis is crucial for intelligent transportation systems.
> Traditional methods rely on background subtraction and handcrafted features, which struggle in complex scenes.
> Recent advances in deep learning particularly one-stage detectors like YOLO and two-stage detectors like Faster R-CNN have dramatically improved detection accuracy and speed.
> In this work, I build a pipeline that not only detects and classifies vehicles (cars, motorcycles, trucks, pedestrians, others) but also tracks each instance to avoid double-counting and estimates its speed via pixel-to-real-world conversion.
```
## Demo 
### Live
https://github.com/user-attachments/assets/7f4edabe-5977-4637-bc1b-d75dcba9bd3e 

### For download
Click -> [⬇️Download](/DEMO/Demo_Video.mp4)
## 🌟 Key Features
- 🎯 **YOLOv8 Object Detection** - Nano variant for real-time performance
- 🔄 **DeepSORT Tracking** - Persistent object IDs with no double-counting
- 📏 **Pixel-to-Speed Conversion** - Real-time km/h estimation
- 🖱️ **Interactive GUI** - Tkinter-based ROI selection
- 📊 **Class-wise Counting** - Vehicles, pedestrians, motorcycles, trucks
- 📈 **Accuracy Reporting** - Automatic JSON report generation

## 📦 Installation
```bash
git clone https://github.com/nouman-x-ahmad/Vehicle-and-Pedestrian-Detection-Count
cd Vehicle-and-Pedestrian-Detection-Count/Code
pip install -r requirement/requirements.txt
```

## 🚀 Usage
```bash
python main.py
```
### 🪜 Workflow
```markdown
> Select MP4 video file
> Draw ROI region on first frame
> System processes video in real-time
> View counts and speeds in output window
```
## 🧠 System Architecture
```mermaid
graph TD
    A[Video Input] --> B{GUI}
    B -->|Select ROI| C[YOLOv8 Detection]
    C --> D[DeepSORT Tracking]
    D --> E[Class Counting]
    D --> F[Speed Estimation]
    E --> G[UI Dashboard]
    F --> G
    G --> H[Accuracy Report]
```

## 🔧 Modules Overview

### 🖼️ GUI Interface
```mermaid
flowchart TB
    A[Start] --> B[Load Video]
    B --> C[Display First Frame]
    C --> D[User Draws ROI]
    D --> E[Start Processing]
    E --> F[Real-time Analysis]
    F --> G[Generate Report]
```

### ⚙️ Processing Pipeline
```mermaid
sequenceDiagram
    participant User
    participant GUI
    participant YOLOv8
    participant DeepSORT
    participant SpeedCalc
    
    User->>GUI: Select video file
    GUI->>User: Show first frame
    User->>GUI: Draw ROI region
    GUI->>YOLOv8: Send ROI frames
    YOLOv8->>DeepSORT: Detections + Classes
    DeepSORT->>SpeedCalc: Tracked positions
    SpeedCalc->>GUI: km/h values
    GUI->>User: Display real-time results
```

### 🔍 Detection Workflow
```mermaid
graph LR
    A[Input Frame] --> B[YOLOv8 Inference]
    B --> C{Confidence Check}
    C -->|High confidence| D[Class Mapping]
    C -->|Low confidence| E[Discard]
    D --> F[Aspect Ratio Check]
    F -->|Wide pedestrian| G[Relabel as motorcycle]
    F -->|Normal| H[Output Detection]
```

## 📊 Class Mapping Table
| COCO ID | Original Class | Mapped Class | Confidence Threshold | Special Handling |
|---------|----------------|--------------|----------------------|------------------|
| 0       | Person         | Pedestrian   | 0.3                  | None |
| 1       | Bicycle        | Motorcycle   | 0.2                  | Lower threshold |
| 2       | Car            | Car          | 0.3                  | None |
| 3       | Motorcycle     | Motorcycle   | 0.2                  | Lower threshold |
| 5       | Bus            | Truck        | 0.3                  | Relabel |
| 7       | Truck          | Truck        | 0.3                  | None |
| Others  | Any            | Rest         | 0.3                  | None |

## 📐 Speed Calculation Formula
Speed (km/h) is calculated using:

```math
v = \frac{\Delta_{\text{pixels}} \times \text{scale}}{\Delta t} \times 3.6
```
Where:
- `Δ_pixels` = Distance traveled in pixels
- `scale` = 1/√(8×20) ft/pixel (conversion factor)
- `Δt` = Time between frames (seconds)
- `3.6` = Conversion factor from m/s to km/h

## 📝 Sample Output Report
```json
{
  "car": {
    "predicted": 42,
    "ground_truth": 40,
    "accuracy_pct": 95.0
  },
  "truck": {
    "predicted": 8,
    "ground_truth": 8,
    "accuracy_pct": 100.0
  }
}
```

## 🚧 Future Work

- **Future Improvements:**
  - Automatic scale calibration
  - Multi-camera support
  - Web-based interface (Flask)
  - Pedestrian trajectory analysis

## 📚 Dependencies
```mermaid
graph LR
    A[Core] --> B[ultralytics]
    A --> C[opencv-python]
    A --> D[deep_sort_realtime]
    A --> E[tkinter]
```

## 🙏 Credits
Developed by [Nouman Ahmad](https://github.com/nouman-x-ahmad)
```
This project is licensed under the MIT License - see the LICENSE file for details.
