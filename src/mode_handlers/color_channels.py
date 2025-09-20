import cv2
from cv2.typing import MatLike

from .base import BaseModeHandler
from .trackers import ContrastBrightnessTracker


class ColorChannelsHandler(BaseModeHandler):
    # For default submode
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)
        self.cb_tracker = ContrastBrightnessTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = self.cb_tracker.apply(frame)
        return display_frame


class RedChannelHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)
        self.cb_tracker = ContrastBrightnessTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = frame.copy()
        display_frame[:, :, 0] = 0
        display_frame[:, :, 1] = 0
        display_frame = self.cb_tracker.apply(display_frame)
        return display_frame


class GreenChannelHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)
        self.cb_tracker = ContrastBrightnessTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = frame.copy()
        display_frame[:, :, 0] = 0
        display_frame[:, :, 2] = 0
        display_frame = self.cb_tracker.apply(display_frame)
        return display_frame


class BlueChannelHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)
        self.cb_tracker = ContrastBrightnessTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = frame.copy()
        display_frame[:, :, 1] = 0
        display_frame[:, :, 2] = 0
        display_frame = self.cb_tracker.apply(display_frame)
        return display_frame


class GrayScaleHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)
        self.cb_tracker = ContrastBrightnessTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        display_frame = self.cb_tracker.apply(display_frame)
        return display_frame
