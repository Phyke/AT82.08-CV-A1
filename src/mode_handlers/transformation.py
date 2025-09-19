import cv2 as cv
import numpy as np
from cv2.typing import MatLike

from mode_handlers.base import BaseModeHandler


class TransformationHandler(BaseModeHandler):
    def setup_window(self, window_name: str):
        cv.destroyWindow(window_name)
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)

    def process_frame(self, frame: MatLike, submode: str) -> MatLike:
        if submode == "Logarithmic":
            log_image = np.log(frame.astype(np.float32) + 1)
            log_image = log_image / np.log(256) * 255
            return log_image.astype(np.uint8)
        elif submode == "Exponential":
            alpha = 0.01
            exp_image = np.exp(alpha * frame.astype(np.float32)) - 1
            exp_image = exp_image / (np.exp(alpha * 255) - 1) * 255
            return exp_image.astype(np.uint8)
        elif submode == "Power-law":
            gamma = 0.5
            power_image = np.power(frame.astype(np.float32) / 255, gamma) * 255
            return power_image.astype(np.uint8)
        elif submode == "Thresholding":
            threshold = 100
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            _, thresh_image = cv.threshold(gray, threshold, 255, cv.THRESH_BINARY)
            return thresh_image
        elif submode == "Negative":
            return 255 - frame
        else:
            return frame
