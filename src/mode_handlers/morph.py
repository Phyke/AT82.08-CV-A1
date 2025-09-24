import cv2
import numpy as np
from cv2.typing import MatLike

from .base import BaseModeHandler
from .trackers import IntensityThresholdTracker, KernelSize3579Tracker


def binarize(frame: MatLike, intensity_threshold: int) -> MatLike:
    # Convert to grayscale if not already
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame
    _, binary = cv2.threshold(gray, intensity_threshold, 255, cv2.THRESH_BINARY)
    return binary


class MorphologicalHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name,
        control_window_name,
        main_window_width,
        main_window_height,
        have_control_window=True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.threshold_tracker = IntensityThresholdTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        intensity_threshold = self.threshold_tracker.get_threshold()
        binary = binarize(frame, intensity_threshold)
        return binary


class ErosionHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name,
        control_window_name,
        main_window_width,
        main_window_height,
        have_control_window=True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernel_tracker = KernelSize3579Tracker(control_window_name)
        self.threshold_tracker = IntensityThresholdTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        intensity_threshold = self.threshold_tracker.get_threshold()
        binary = binarize(frame, intensity_threshold)
        kernel_size = self.kernel_tracker.get_kernel_size()
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        eroded = cv2.erode(binary, kernel, iterations=1)
        return eroded


class DilationHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name,
        control_window_name,
        main_window_width,
        main_window_height,
        have_control_window=True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernel_tracker = KernelSize3579Tracker(control_window_name)
        self.threshold_tracker = IntensityThresholdTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        intensity_threshold = self.threshold_tracker.get_threshold()
        binary = binarize(frame, intensity_threshold)
        kernel_size = self.kernel_tracker.get_kernel_size()
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dilated = cv2.dilate(binary, kernel, iterations=1)
        return dilated


class OpeningHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name,
        control_window_name,
        main_window_width,
        main_window_height,
        have_control_window=True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernel_tracker = KernelSize3579Tracker(control_window_name)
        self.threshold_tracker = IntensityThresholdTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        intensity_threshold = self.threshold_tracker.get_threshold()
        binary = binarize(frame, intensity_threshold)
        kernel_size = self.kernel_tracker.get_kernel_size()
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        return opened


class ClosingHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name,
        control_window_name,
        main_window_width,
        main_window_height,
        have_control_window=True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernel_tracker = KernelSize3579Tracker(control_window_name)
        self.threshold_tracker = IntensityThresholdTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        intensity_threshold = self.threshold_tracker.get_threshold()
        binary = binarize(frame, intensity_threshold)
        kernel_size = self.kernel_tracker.get_kernel_size()
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        return closed


class MorphologicalGradientHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name,
        control_window_name,
        main_window_width,
        main_window_height,
        have_control_window=True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernel_tracker = KernelSize3579Tracker(control_window_name)
        self.threshold_tracker = IntensityThresholdTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        intensity_threshold = self.threshold_tracker.get_threshold()
        binary = binarize(frame, intensity_threshold)
        kernel_size = self.kernel_tracker.get_kernel_size()
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
        return gradient


class TopHatHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name,
        control_window_name,
        main_window_width,
        main_window_height,
        have_control_window=True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernel_tracker = KernelSize3579Tracker(control_window_name)
        self.threshold_tracker = IntensityThresholdTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        intensity_threshold = self.threshold_tracker.get_threshold()
        binary = binarize(frame, intensity_threshold)
        kernel_size = self.kernel_tracker.get_kernel_size()
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        tophat = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, kernel)
        return tophat


class BlackHatHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name,
        control_window_name,
        main_window_width,
        main_window_height,
        have_control_window=True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernel_tracker = KernelSize3579Tracker(control_window_name)
        self.threshold_tracker = IntensityThresholdTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        intensity_threshold = self.threshold_tracker.get_threshold()
        binary = binarize(frame, intensity_threshold)
        kernel_size = self.kernel_tracker.get_kernel_size()
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        blackhat = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, kernel)
        return blackhat
