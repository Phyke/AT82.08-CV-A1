import cv2
import numpy as np
from cv2.typing import MatLike

from .base import BaseModeHandler
from .trackers import HarrisParamsTracker


class CornerDetectionHandler(BaseModeHandler):
    # For default submode
    def setup_window(self, main_window_name, control_window_name, main_window_width, main_window_height):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window=True,
        )
        self.tracker = HarrisParamsTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype("float32")

        block_size = self.tracker.get_block_size()
        sobel_ksize = self.tracker.get_sobel_ksize()  # Aperture size for Sobel operator
        dilate_ksize = self.tracker.get_dilate_ksize()  # Bigger kernel, bigger dots
        threshold = self.tracker.get_threshold()  # lower threshold means more corners

        # Harris corner detection
        harris_response = cv2.cornerHarris(gray, blockSize=block_size, ksize=sobel_ksize, k=0.04)
        kernel = np.ones((dilate_ksize, dilate_ksize), np.uint8)
        harris_response_dilated = cv2.dilate(harris_response, kernel)
        corners = frame.copy()
        # Thresholding to get the corners
        threshold_value = threshold * harris_response_dilated.max()
        corners[harris_response_dilated > threshold_value] = [0, 0, 255]  # Mark corners in red
        return corners
