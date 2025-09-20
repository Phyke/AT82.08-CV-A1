import cv2
import numpy as np
from cv2.typing import MatLike

from .base import BaseModeHandler
from .trackers import CannyThresholdTracker, HoughCirclesParamsTracker, HoughLinesParamsTracker


class HoughLinesHandler(BaseModeHandler):
    def setup_window(self, main_window_name, control_window_name, main_window_width, main_window_height):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)
        self.canny_tracker = CannyThresholdTracker(control_window_name)
        self.hough_tracker = HoughLinesParamsTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canny_low, canny_high = self.canny_tracker.get_thresholds()
        hough_threshold = self.hough_tracker.get_threshold()
        edges = cv2.Canny(gray, canny_low, canny_high, L2gradient=True)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, hough_threshold)
        hough_image = frame.copy()
        if lines is not None:
            for rho, theta in lines[:, 0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(hough_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return hough_image


class HoughCirclesHandler(BaseModeHandler):
    def setup_window(self, main_window_name, control_window_name, main_window_width, main_window_height):
        super().setup_window(main_window_name, control_window_name, main_window_width, main_window_height)
        self.hough_tracker = HoughCirclesParamsTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)

        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=self.hough_tracker.dp,
            minDist=self.hough_tracker.min_dist,
            param1=self.hough_tracker.param1,
            param2=self.hough_tracker.param2,
            minRadius=self.hough_tracker.min_radius,
            maxRadius=self.hough_tracker.max_radius,
        )
        hough_image = frame.copy()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(hough_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(hough_image, (i[0], i[1]), 2, (0, 0, 255), 3)
        return hough_image
