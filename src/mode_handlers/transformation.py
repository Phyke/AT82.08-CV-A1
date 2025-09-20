import cv2
import numpy as np
from cv2.typing import MatLike

from .base import BaseModeHandler


class TransformationHandler(BaseModeHandler):
    # For default submode
    def process_frame(self, frame: MatLike) -> MatLike:
        return frame


class LogarithmicHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)

    def process_frame(self, frame: MatLike) -> MatLike:
        log_image = np.log(frame.astype(np.float32) + 1)
        log_image = log_image / np.log(256) * 255
        return log_image.astype(np.uint8)


class ExponentialHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)

    def process_frame(self, frame: MatLike) -> MatLike:
        alpha = 0.01
        exp_image = np.exp(alpha * frame.astype(np.float32)) - 1
        exp_image = exp_image / (np.exp(alpha * 255) - 1) * 255
        return exp_image.astype(np.uint8)


class PowerLawHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)

    def process_frame(self, frame: MatLike) -> MatLike:
        gamma = 0.5
        power_image = np.power(frame.astype(np.float32) / 255, gamma) * 255
        return power_image.astype(np.uint8)


class ThresholdingHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)

    def process_frame(self, frame: MatLike) -> MatLike:
        threshold = 100
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh_image = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return thresh_image


class NegativeHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)

    def process_frame(self, frame: MatLike) -> MatLike:
        return 255 - frame
