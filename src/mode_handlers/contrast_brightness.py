import cv2
import numpy as np
from cv2.typing import MatLike

from .base import BaseModeHandler
from .trackers import BrightnessTracker, ContrastTracker


class ContrastBrightnessHistogramHandler(BaseModeHandler):
    def __init__(
        self,
        bins: int = 256,
        hist_height: int = 300,
        hist_width: int = 512,
    ):
        super().__init__()
        # Histogram config
        self.bins = bins
        self.hist_height = hist_height
        self.hist_width = hist_width
        self.histogram_window_name = "Histogram"

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
            have_control_window=have_control_window,
        )
        self.contrast_tracker = ContrastTracker(control_window_name)
        self.brightness_tracker = BrightnessTracker(control_window_name)

        # Histogram window
        self.hist_width = max(self.hist_width, main_window_width // 2)
        self.hist_height = max(self.hist_height, min(400, main_window_height))
        cv2.namedWindow(self.histogram_window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.histogram_window_name, self.hist_width, self.hist_height)

    # Histogram helpers
    def _compute_channel_hist(self, image: np.ndarray, channel_index: int) -> np.ndarray:
        hist = cv2.calcHist([image], [channel_index], None, [self.bins], [0, 256])
        cv2.normalize(hist, hist, 0, self.hist_height, cv2.NORM_MINMAX)
        return hist.flatten()

    def _render_histogram(self, hists: list[np.ndarray], colors: list[tuple]) -> np.ndarray:
        canvas = np.zeros((self.hist_height, self.hist_width, 3), dtype=np.uint8)
        bin_w = max(1, int(self.hist_width / self.bins))
        for hist, color in zip(hists, colors):
            for i in range(1, self.bins):
                x1 = (i - 1) * bin_w
                x2 = i * bin_w
                y1 = self.hist_height - int(hist[i - 1])
                y2 = self.hist_height - int(hist[i])
                cv2.line(canvas, (x1, y1), (x2, y2), color, 1, cv2.LINE_AA)
        return canvas

    def _update_histogram(self, frame: np.ndarray):
        if frame is None:
            return
        if len(frame.shape) == 2 or frame.shape[2] == 1:
            gray = frame if len(frame.shape) == 2 else frame[:, :, 0]
            hist = self._compute_channel_hist(gray, 0)
            hist_img = self._render_histogram([hist], [(200, 200, 200)])
        else:
            hists = [self._compute_channel_hist(frame, i) for i in range(3)]
            hist_img = self._render_histogram(
                hists,
                [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
            )
        cv2.imshow(self.histogram_window_name, hist_img)

    def process_frame(self, frame: MatLike) -> MatLike:
        if frame is None:
            return frame
        # Apply brightness / contrast using trackers
        brightness = self.brightness_tracker.get_brightness()
        contrast = self.contrast_tracker.get_contrast()
        adjusted = cv2.convertScaleAbs(frame, alpha=contrast / 50.0, beta=brightness - 50)
        self._update_histogram(adjusted)
        return adjusted
