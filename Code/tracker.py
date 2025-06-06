from deep_sort_realtime.deepsort_tracker import DeepSort

class Tracker:
    def __init__(self):
        self.tracker = DeepSort(max_age=30)
        self.counted_ids = set()
        self.counts = {'pedestrian': 0, 'car': 0, 'motorcycle': 0, 'truck': 0, 'rest': 0}

    def update_tracks(self, detections, frame):
        tracks = self.tracker.update_tracks(detections, frame=frame)
        for det, track in zip(detections, tracks):
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            _, _, label = det
            if track_id not in self.counted_ids:
                self.counted_ids.add(track_id)
                # increment appropriate bucket
                if label in self.counts:
                    self.counts[label] += 1
        return tracks

    def get_counts(self):
        return self.counts