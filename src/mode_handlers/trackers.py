import cv2 as cv
from cv2.typing import MatLike


class ContrastBrightnessTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.brightness = 50
        self.contrast = 50
        cv.createTrackbar(
            "Brightness",
            self.window_name,
            self.brightness,
            100,
            self.on_brightness_change,
        )
        cv.createTrackbar(
            "Contrast",
            self.window_name,
            self.contrast,
            100,
            self.on_contrast_change,
        )

    def on_brightness_change(self, value: int):
        self.brightness = value

    def on_contrast_change(self, value: int):
        self.contrast = value

    def apply(self, frame: MatLike) -> MatLike:
        adjusted_frame = cv.convertScaleAbs(
            frame, alpha=self.contrast / 50, beta=self.brightness - 50
        )
        return adjusted_frame
