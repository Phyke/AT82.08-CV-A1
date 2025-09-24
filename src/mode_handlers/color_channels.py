import cv2
from cv2.typing import MatLike

from .base import BaseModeHandler


class RGBHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        return frame


class RedChannelHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = frame.copy()
        display_frame[:, :, 0] = 0  # Zero out Blue channel
        display_frame[:, :, 1] = 0  # Zero out Green channel
        return display_frame


class GreenChannelHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = frame.copy()
        display_frame[:, :, 0] = 0  # Zero out Blue channel
        display_frame[:, :, 2] = 0  # Zero out Red channel
        return display_frame


class BlueChannelHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = frame.copy()
        display_frame[:, :, 1] = 0  # Zero out Green channel
        display_frame[:, :, 2] = 0  # Zero out Red channel
        return display_frame


class GrayScaleHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return display_frame


class HSVHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        return display_frame
