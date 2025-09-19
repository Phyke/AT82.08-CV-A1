import cv2 as cv
from cv2.typing import MatLike

from mode_handlers import BaseModeHandler, mode_map, modes2keys

cap = cv.VideoCapture(0)
cv.namedWindow("frame", cv.WINDOW_NORMAL)

mode = "Default"
submode = "Default"
last_key = -1
current_handler: BaseModeHandler = None  # Track the current mode handler


def recreate_window_default():
    cv.destroyWindow("frame")
    cv.namedWindow("frame", cv.WINDOW_NORMAL)


def handle_key_mode():
    global mode, submode, last_key, current_handler
    polling_key = cv.waitKey(1) & 0xFF
    if polling_key != 0xFF:
        last_key = polling_key
        print("last_key code:", last_key)
        print(
            "last_key char:",
            chr(last_key) if 32 <= last_key <= 126 else "",
            f"({last_key})",
        )

        if last_key == 27:  # ESC
            return False

        # Allow switching modes at any time
        if chr(last_key) in mode_map.keys():
            mode_key = chr(last_key)
            mode_info = mode_map[mode_key]
            mode = mode_info["name"]
            submode = "Default"

            handler_class = mode_info.get("handler_class")
            if handler_class:
                current_handler = handler_class()
                current_handler.setup_window("frame")
            else:
                current_handler = None
                recreate_window_default()
            print(f"Switched to mode: {mode}")

        elif mode != "Default":
            current_mode_key = modes2keys[mode.lower()]
            available_submodes = mode_map[current_mode_key]["submodes"]
            if chr(last_key) in available_submodes:
                submode = available_submodes[chr(last_key)]
                print(f"Switched to submode: {submode}")
    return True


def handle_mode(frame: MatLike):
    global current_handler, submode
    if mode == "Default":
        display_frame = frame
    elif current_handler:
        display_frame = current_handler.process_frame(frame, submode)
    else:
        display_frame = frame
    return display_frame


def put_display_text(frame: MatLike):
    cv.putText(
        img=frame,
        text=f"Mode: {mode}, Submode: {submode}",
        org=(10, 30),
        fontFace=cv.FONT_HERSHEY_SIMPLEX,
        fontScale=1,
        color=255,
        thickness=2,
        lineType=cv.LINE_AA,
    )
    return frame


while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    not_backspace = handle_key_mode()
    if not_backspace is False:
        break

    display_frame = handle_mode(frame)
    display_frame = put_display_text(display_frame)

    cv.imshow("frame", display_frame)

cap.release()
cv.destroyAllWindows()
