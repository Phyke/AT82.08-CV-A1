import cv2
import numpy as np
from cv2.typing import MatLike

from .base import BaseModeHandler


class PanoramaHandler(BaseModeHandler):
    def __init__(self):
        super().__init__()
        self.captured_images = []
        self.panorama = None  # Store stitched result
        self.stitch_error = False

    def setup_window(
        self,
        *args,
        **kwargs,
    ):
        super().setup_window(have_control_window=False, *args, **kwargs)
        cv2.namedWindow("Panorama Captures", cv2.WINDOW_NORMAL)
        main_window_width = kwargs.get("main_window_width", 640)
        main_window_height = kwargs.get("main_window_height", 480)
        cv2.resizeWindow("Panorama Captures", main_window_width, main_window_height)

    def process_frame(self, frame: MatLike) -> MatLike:
        # Show stitched panorama if available
        if self.panorama is not None:
            cv2.imshow("Panorama Captures", self.panorama)
        elif self.stitch_error:
            shape = frame.shape
            dtype = frame.dtype
            error_img = np.zeros(shape, dtype)
            cv2.putText(
                error_img,
                "Stitching failed",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                error_img,
                "Change angle and press capture again",
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
            cv2.imshow("Panorama Captures", error_img)
        else:
            empty_img = np.zeros_like(frame)
            cv2.imshow("Panorama Captures", empty_img)
        return frame

    def handle_key(self, key, frame: MatLike):
        if key == ord(" ") and len(self.captured_images) < 10:
            print("Captured image for panorama.")
            self.captured_images.append(frame.copy())
            # Stitch if at least 2 images
            if len(self.captured_images) >= 2:
                stitcher = cv2.Stitcher_create()
                status, pano = stitcher.stitch(self.captured_images)
                if status == cv2.Stitcher_OK:
                    self.panorama = pano
                    self.stitch_error = False
                else:
                    self.panorama = None
                    self.stitch_error = True

        elif key == ord("r"):
            print("Resetting captured images.")
            self.captured_images = []
            self.panorama = None
            self.stitch_error = False
