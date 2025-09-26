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
    # Common style
    color_fg = (0, 0, 0)  # black text
    color_bg = (255, 255, 255)  # white background
    pad_x, pad_y = 5, 3
    font_face = cv2.FONT_HERSHEY_SIMPLEX

    # Mode text
    mode_text = f"Mode: {mode}"
    mode_font_scale = 0.7
    mode_thickness = 2
    (mode_w, mode_h), mode_baseline = cv2.getTextSize(mode_text, font_face, mode_font_scale, mode_thickness)
    mode_x, mode_y = 10, 30
    cv2.rectangle(
        frame,
        (mode_x - pad_x, mode_y - mode_h - pad_y),
        (mode_x + mode_w + pad_x, mode_y + mode_baseline + pad_y),
        color_bg,
        -1,
    )
    cv2.putText(
        img=frame,
        text=mode_text,
        org=(mode_x, mode_y),
        fontFace=font_face,
        fontScale=mode_font_scale,
        color=color_fg,
        thickness=mode_thickness,
        lineType=cv2.LINE_AA,
    )

    # Submode text
    submode_text = f"Submode: {submode}"
    submode_font_scale = 0.5
    submode_thickness = 1
    (submode_w, submode_h), submode_baseline = cv2.getTextSize(
        submode_text, font_face, submode_font_scale, submode_thickness
    )
    submode_x, submode_y = 10, 60
    cv2.rectangle(
        frame,
        (submode_x - pad_x, submode_y - submode_h - pad_y),
        (submode_x + submode_w + pad_x, submode_y + submode_baseline + pad_y),
        color_bg,
        -1,
    )
    cv2.putText(
        img=frame,
        text=submode_text,
        org=(submode_x, submode_y),
        fontFace=font_face,
        fontScale=submode_font_scale,
        color=color_fg,
        thickness=submode_thickness,
        lineType=cv2.LINE_AA,
    )

    # Show control hints for submodes in the current mode
    mode_key = modes2keys.get(mode.lower())
    submodes = mode_map.get(mode_key, {}).get("submodes", {})
    hints = [f"{k}: {v['name']}" for k, v in submodes.items()]
    hint_font_scale = 0.45
    hint_thickness = 1

    start_y = 90
    for i, hint in enumerate(hints):
        (text_w, text_h), baseline = cv2.getTextSize(hint, font_face, hint_font_scale, hint_thickness)
        x, y = 10, start_y + i * (text_h + 8)
        cv2.rectangle(frame, (x - pad_x, y - text_h - pad_y), (x + text_w + pad_x, y + baseline + pad_y), color_bg, -1)
        cv2.putText(
            img=frame,
            text=hint,
            org=(x, y),
            fontFace=font_face,
            fontScale=hint_font_scale,
            color=color_fg,
            thickness=hint_thickness,
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
