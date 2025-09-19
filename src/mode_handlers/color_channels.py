import cv2 as cv
from cv2.typing import MatLike

from mode_handlers.base import BaseModeHandler
from mode_handlers.trackers import ContrastBrightnessTracker


class ColorChannelsHandler(BaseModeHandler):
    def __init__(self):
        pass

    def setup_window(self, window_name: str):
        cv.destroyWindow(window_name)
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)
        self.cb_tracker = ContrastBrightnessTracker("frame")

    def process_frame(self, frame: MatLike, submode: str) -> MatLike:
        if submode == "Red channel":
            display_frame = frame.copy()
            display_frame[:, :, 0] = 0
            display_frame[:, :, 1] = 0
        elif submode == "Green channel":
            display_frame = frame.copy()
            display_frame[:, :, 0] = 0
            display_frame[:, :, 2] = 0
        elif submode == "Blue channel":
            display_frame = frame.copy()
            display_frame[:, :, 1] = 0
            display_frame[:, :, 2] = 0
        elif submode == "Gray scale":
            display_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        else:
            display_frame = frame
        display_frame = self.cb_tracker.apply(display_frame)
        return display_frame
