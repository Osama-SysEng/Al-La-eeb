import pytest
import numpy as np
from app.pipelines.cv_pipeline import SkeletalTrackingEngine, BallTrackingEngine, EventDetectionEngine

def test_skeletal_tracking():
    engine = SkeletalTrackingEngine()
    frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    result = engine.process_frame(frame, 0, 0.0)
    assert len(result.keypoints) == 33
    assert result.keypoints[0].name == "nose"

def test_ball_tracking():
    engine = BallTrackingEngine()
    frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    pos, conf = engine.detect_ball(frame)
    assert pos is not None
    assert 0 <= conf <= 1

def test_event_detection():
    engine = EventDetectionEngine()
    from app.pipelines.cv_pipeline import FrameData, Keypoint
    frames = []
    for i in range(100):
        kps = [Keypoint(x=0.5, y=0.5, z=0.0, visibility=0.95, name=f"kp_{j}") for j in range(33)]
        frames.append(FrameData(frame_id=i, timestamp_ms=i*33.33, keypoints=kps))
    events = engine.detect_events(frames)
    assert isinstance(events, list)
