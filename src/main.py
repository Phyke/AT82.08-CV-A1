import cv2
from cv2.typing import MatLike

from mode_handlers.base import BaseModeHandler
from mode_handlers.modes import mode_map, modes2keys

# Get camera frame size
cap = cv2.VideoCapture(0)
ret, test_frame = cap.read()
if not ret:
    raise RuntimeError("Cannot read from camera")
cam_height, cam_width = test_frame.shape[:2]
ratio = cam_width / cam_height
print(f"Camera resolution: {cam_width}x{cam_height}, ratio: {ratio:.2f}")
# My camera is 640x480, so I want to scale to make it bigger
cam_width = int(cam_width * 1.5)
cam_height = int(cam_height * 1.5)
print(f"New Camera resolution: {cam_width}x{cam_height}, ratio: {ratio:.2f}")

scaled_height = cam_width
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", cam_width, cam_height)

# Start with Color Channel mode (mode "1")
mode = "Color Channel"
submode = "RGB"
last_key = -1
current_handler: BaseModeHandler = None  # Track the current submode handler


def recreate_window_default():
    cv2.destroyAllWindows()
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("frame", cam_width, cam_height)


def get_submode_info(mode_key, submode_key):
    mode_info = mode_map[mode_key]
    submode_map = mode_info.get("submodes", {})
    return submode_map.get(submode_key, {"name": "RGB", "handler": None})


def handle_key_mode(frame=None):
    global mode, submode, last_key, current_handler
    polling_key = cv2.waitKey(1) & 0xFF
    if polling_key != 0xFF:
        last_key = polling_key
        print(
            "last_key char:",
            chr(last_key) if 32 <= last_key <= 126 else "",
            f"({last_key})",
        )

        # If current handler has handle_key (e.g., PanoramaHandler), call it
        if (
            current_handler
            and hasattr(current_handler, "handle_key")
            and current_handler.__class__.__name__ == "PanoramaHandler"
        ):
            current_handler.handle_key(last_key, frame)

        if last_key == 27:  # ESC
            return False

        # Allow switching modes at any time
        if chr(last_key) in mode_map.keys():
            mode_key = chr(last_key)
            mode_info = mode_map[mode_key]
            mode = mode_info["name"]
            # Get the first submode name for this mode
            submodes = mode_map[mode_key].get("submodes", {})
            submode = next(iter(submodes.values()))["name"] if submodes else "RGB"

            # Instantiate handler for default submode
            submode_info = get_submode_info(mode_key, "q")
            handler_class = submode_info.get("handler")
            if handler_class:
                current_handler = handler_class()
                current_handler.setup_window("frame", "controls", cam_width, cam_height)
            else:
                current_handler = None
                recreate_window_default()
            print(f"Switched to mode: {mode}")

        # Allow submode switching for all modes with submodes
        else:
            current_mode_key = modes2keys[mode.lower()]
            submodes = mode_map[current_mode_key]["submodes"]
            if chr(last_key) in submodes:
                submode_key = chr(last_key)
                submode_info = submodes[submode_key]
                submode = submode_info["name"]
                handler_class = submode_info.get("handler")
                if handler_class:
                    current_handler = handler_class()
                    current_handler.setup_window("frame", "controls", cam_width, cam_height)
                else:
                    current_handler = None
                    recreate_window_default()
                print(f"Switched to submode: {submode}")
    return True


def handle_mode(frame: MatLike):
    global current_handler, submode
    if current_handler:
        display_frame = current_handler.process_frame(frame)
    else:
        display_frame = frame
    # No resizing, just return the frame as-is
    return display_frame


def put_display_text(frame: MatLike):
    cv2.putText(
        img=frame,
        text=f"Mode: {mode}",
        org=(10, 30),  # Top-left corner
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.7,
        color=255,
        thickness=2,
        lineType=cv2.LINE_AA,
    )
    cv2.putText(
        img=frame,
        text=f"Submode: {submode}",
        org=(10, 60),  # Below the mode text
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.5,
        color=255,
        thickness=1,
        lineType=cv2.LINE_AA,
    )
    return frame


while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    not_backspace = handle_key_mode(frame)
    if not_backspace is False:
        break

    display_frame = handle_mode(frame)
    display_frame = put_display_text(display_frame)

    cv2.imshow("frame", display_frame)

cap.release()
cv2.destroyAllWindows()
cv2.destroyAllWindows()
