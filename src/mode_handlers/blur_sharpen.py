import cv2 as cv
import numpy as np
from cv2.typing import MatLike

from mode_handlers.base import BaseModeHandler


class BlurSharpenHandler(BaseModeHandler):
    def setup_window(self, window_name: str):
        cv.destroyWindow(window_name)
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)

    def process_frame(self, frame: MatLike, submode: str) -> MatLike:
        if submode == "Averaging":
            return cv.blur(frame, (7, 7))
        elif submode == "Gaussian":
            sigma = 1
            kernel_size = int(np.ceil(2 * np.pi * sigma))
            if kernel_size % 2 == 0:
                kernel_size += 1
            kernel_size = max(3, kernel_size)
            return cv.GaussianBlur(frame, (kernel_size, kernel_size), sigmaX=sigma)
        elif submode == "Median":
            return cv.medianBlur(frame, 7)
        elif submode == "Bilateral":
            return cv.bilateralFilter(frame, d=7, sigmaColor=75, sigmaSpace=75)
        elif submode == "Sharpening":
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            return cv.filter2D(frame, -1, kernel)
        else:
            return frame
