from cv2.typing import MatLike


class BaseModeHandler:
    def setup_window(self, window_name: str):
        """Set up the window and any trackbars needed for this mode."""
        raise NotImplementedError

    def process_frame(self, frame: MatLike, submode: str) -> MatLike:
        """Process the frame according to the mode and submode."""
        raise NotImplementedError
