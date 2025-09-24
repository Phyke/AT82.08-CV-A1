import cv2
from cv2.typing import MatLike

from .base import BaseModeHandler
from .trackers import TranslateTracker


class TranslateHandler(BaseModeHandler):
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
        have_control_window=True,
    ):
        super().setup_window(
            main_window_name,
            control_window_name,
            main_window_width,
            main_window_height,
            have_control_window,
        )
        self.translate_tracker = TranslateTracker(control_window_name)

    def process_frame(self, frame: MatLike) -> MatLike:
        height, width = frame.shape[:2]
        center = (width // 2, height // 2)

        # Get transformation parameters
        translate_x = self.translate_tracker.get_translate_x()
        translate_y = self.translate_tracker.get_translate_y()
        angle = self.translate_tracker.get_rotate_angle()
        scale = self.translate_tracker.get_scale_factor()

        # Create rotation and scale matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

        # Add translation
        rotation_matrix[0, 2] += translate_x
        rotation_matrix[1, 2] += translate_y

        # Apply transformation
        transformed_frame = cv2.warpAffine(frame, rotation_matrix, (width, height))

        return transformed_frame
