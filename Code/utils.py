import cv2

def estimate_speed(distance_ft, time_s):
    return (distance_ft / 1000) / (time_s / 3600)  # km/h


def draw_ui(frame, counts):
    text = (
        f"Pedestrians: {counts['pedestrian']} | "
        f"Cars: {counts['car']} | "
        f"Motorcycles: {counts['motorcycle']} | "
        f"Trucks: {counts['truck']} | "
        f"Rest: {counts['rest']}"
    )
    cv2.putText(frame, text, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)