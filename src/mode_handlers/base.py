import cv2
from cv2.typing import MatLike


class BaseModeHandler:
    def setup_window(
        self,
        main_window_name: str,
        control_window_name: str,
        main_window_width: int,
        main_window_height: int,
        have_control_window: bool = False,
    ):
        """Set up the window and any trackbars needed for this mode."""
        cv2.destroyAllWindows()
        cv2.namedWindow(main_window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(main_window_name, main_window_width, main_window_height)
        if have_control_window:
            cv2.namedWindow(control_window_name, cv2.WINDOW_AUTOSIZE)

    def process_frame(self, frame: MatLike) -> MatLike:
        """Process the frame according to the submode."""
        raise NotImplementedError
