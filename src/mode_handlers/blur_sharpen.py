import cv2
import numpy as np
from cv2.typing import MatLike

from .base import BaseModeHandler
from .trackers import BilateralSigmaTracker, KernelSizeTracker, SigmaTracker


class BlurSharpenHandler(BaseModeHandler):
    # For default submode
    def process_frame(self, frame: MatLike) -> MatLike:
        return frame


class AverageBlurHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
        have_control_window: bool = True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernelsize_tracker = KernelSizeTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        kernel_size = self.kernelsize_tracker.get_effective_kernel_size()
        return cv2.blur(frame, (kernel_size, kernel_size))


class GaussianBlurHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
        have_control_window: bool = True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernelsize_tracker = KernelSizeTracker(control_window_name)
        self.sigma_tracker = SigmaTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        sigma = self.sigma_tracker.get_sigma()
        kernel_size = self.kernelsize_tracker.get_effective_kernel_size()
        return cv2.GaussianBlur(frame, (kernel_size, kernel_size), sigmaX=sigma)


class GaussianBlurAutoHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
        have_control_window: bool = True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.sigma_tracker = SigmaTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        sigma = self.sigma_tracker.get_sigma()
        kernel_size = self.get_effective_kernel_size_for_gaussian(sigma)
        return cv2.GaussianBlur(frame, (kernel_size, kernel_size), sigmaX=sigma)

    def get_effective_kernel_size_for_gaussian(self, sigma: int) -> int:
        kernel_size = int(np.ceil(2 * np.pi * sigma))
        if kernel_size % 2 == 0:
            kernel_size += 1
        return max(3, kernel_size)


class MedianBlurHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
        have_control_window: bool = True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernelsize_tracker = KernelSizeTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        kernel_size = self.kernelsize_tracker.get_effective_kernel_size()
        return cv2.medianBlur(frame, kernel_size)


class BilateralBlurHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
        have_control_window: bool = True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.kernelsize_tracker = KernelSizeTracker(control_window_name)
        self.bilateral_sigma_tracker = BilateralSigmaTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        kernel_size = self.kernelsize_tracker.get_effective_kernel_size()
        sigma_color = self.bilateral_sigma_tracker.get_sigma_color()
        sigma_space = self.bilateral_sigma_tracker.get_sigma_space()
        return cv2.bilateralFilter(frame, d=kernel_size, sigmaColor=sigma_color, sigmaSpace=sigma_space)


class SharpenHandler(BaseModeHandler):
    def process_frame(self, frame: MatLike) -> MatLike:
        kernel = np.array(
            [
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0],
            ]
        )
        return cv2.filter2D(frame, -1, kernel)
