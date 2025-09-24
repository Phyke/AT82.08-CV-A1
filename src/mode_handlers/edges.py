import cv2
import numpy as np
from cv2.typing import MatLike

from .base import BaseModeHandler
from .trackers import CannyThresholdTracker


class EdgeDetectionHandler(BaseModeHandler):
    # For default submode
    def process_frame(self, frame: MatLike) -> MatLike:
        return frame


class RobertsXCrossHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        kernel = np.array([[0, 1], [-1, 0]])
        image_edges_x = cv2.filter2D(frame, -1, kernel)
        return image_edges_x


class RobertsYCrossHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        kernel = np.array(
            [
                [1, 0],
                [0, -1],
            ]
        )
        image_edges_y = cv2.filter2D(frame, -1, kernel)
        return image_edges_y


class RobertsXYCrossHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        kernel_x = np.array(
            [
                [0, 1],
                [-1, 0],
            ]
        )
        kernel_y = np.array(
            [
                [1, 0],
                [0, -1],
            ]
        )
        image_edges_x = cv2.filter2D(frame, -1, kernel_x)
        image_edges_y = cv2.filter2D(frame, -1, kernel_y)
        image_edges = cv2.add(image_edges_x, image_edges_y)
        return image_edges


class PrewittXHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        kernel = np.array(
            [
                [-1, 0, 1],
                [-1, 0, 1],
                [-1, 0, 1],
            ]
        )
        image_edges_x = cv2.filter2D(frame, -1, kernel)
        return image_edges_x


class PrewittYHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        kernel = np.array(
            [
                [1, 1, 1],
                [0, 0, 0],
                [-1, -1, -1],
            ]
        )
        image_edges_y = cv2.filter2D(frame, -1, kernel)
        return image_edges_y


class PrewittXYHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        kernel_x = np.array(
            [
                [-1, 0, 1],
                [-1, 0, 1],
                [-1, 0, 1],
            ]
        )
        kernel_y = np.array(
            [
                [1, 1, 1],
                [0, 0, 0],
                [-1, -1, -1],
            ]
        )
        image_edges_x = cv2.filter2D(frame, -1, kernel_x)
        image_edges_y = cv2.filter2D(frame, -1, kernel_y)
        image_edges = cv2.add(image_edges_x, image_edges_y)
        return image_edges


class SobelXHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        # cv.Sobel(frame, cv.CV_64F, 1, 0, ksize=3)
        kernel = np.array(
            [
                [-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1],
            ]
        )
        image_edges_x = cv2.filter2D(frame, -1, kernel)
        return image_edges_x


class SobelYHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        # cv.Sobel(frame, cv.CV_64F, 0, 1, ksize=3)
        kernel = np.array(
            [
                [1, 2, 1],
                [0, 0, 0],
                [-1, -2, -1],
            ]
        )
        image_edges_y = cv2.filter2D(frame, -1, kernel)
        return image_edges_y


class SobelHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        # cv.Sobel(frame, cv.CV_64F, 1, 1, ksize=3)
        kernel_x = np.array(
            [
                [-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1],
            ]
        )
        kernel_y = np.array(
            [
                [1, 2, 1],
                [0, 0, 0],
                [-1, -2, -1],
            ]
        )
        image_edges_x = cv2.filter2D(frame, -1, kernel_x)
        image_edges_y = cv2.filter2D(frame, -1, kernel_y)
        image_edges = cv2.add(image_edges_x, image_edges_y)
        return image_edges


class LaplacianHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        return cv2.Laplacian(frame, cv2.CV_64F)


class CannyHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window=True,
        )
        self.canny_tracker = CannyThresholdTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        threshold1, threshold2 = self.canny_tracker.get_thresholds()
        return cv2.Canny(frame, threshold1, threshold2, L2gradient=True)
