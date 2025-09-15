import cv2 as cv
from cv2.typing import MatLike

cap = cv.VideoCapture(0)
cv.namedWindow("frame", cv.WINDOW_NORMAL)

mode = "default"
submode = "n/a"
last_key = -1


def recreate_window_default():
    cv.destroyWindow("frame")
    cv.namedWindow("frame", cv.WINDOW_NORMAL)


def recreate_window_with_brightness_and_contrast():
    cv.destroyWindow("frame")
    cv.namedWindow("frame", cv.WINDOW_NORMAL)
    cv.createTrackbar("Brightness", "frame", 50, 100, lambda x: None)
    cv.createTrackbar("Contrast", "frame", 50, 100, lambda x: None)


def apply_trackbar_values(frame: MatLike):
    brightness = cv.getTrackbarPos("Brightness", "frame")
    contrast = cv.getTrackbarPos("Contrast", "frame")
    # Apply brightness and contrast adjustments (dummy implementation)
    adjusted_frame = cv.convertScaleAbs(
        frame, alpha=contrast / 50, beta=brightness - 50
    )
    return adjusted_frame


def handle_key_mode():
    global mode, submode, last_key
    polling_key = cv.waitKey(1) & 0xFF
    # cannot use polling_key directly it will reset the -1 every loop
    # because it results in 1 frame per key press (mashing key will result in disco lights)
    if polling_key != 0xFF:
        last_key = polling_key  # store last key pressed for conditions below
        print("last_key code:", last_key)
        print(
            "last_key char:",
            chr(last_key) if 32 <= last_key <= 126 else "",
            f"({last_key})",
        )

        if last_key == 27:  # ESC
            return False

        # Bypass every mode if 0 is pressed
        if last_key == ord("0"):
            recreate_window_default()
            mode = "default"
            submode = "n/a"
            print("Default mode")

        # If in default mode, allow switching to other modes
        elif mode == "default":
            if last_key == ord("1"):
                recreate_window_with_brightness_and_contrast()
                mode = "color channels"
                submode = "n/a"

            elif last_key == ord("2"):
                recreate_window_with_brightness_and_contrast()
                mode = "grayscale"
                submode = "n/a"

        elif mode == "color channels":
            if last_key == ord("r"):
                submode = "red channel"
            elif last_key == ord("g"):
                submode = "green channel"
            elif last_key == ord("b"):
                submode = "blue channel"
    return True


def handle_mode(frame: MatLike):
    # Build display_frame fresh every loop based on mode/submode
    if mode == "default":
        display_frame = frame
    elif mode == "grayscale":
        display_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        display_frame = apply_trackbar_values(display_frame)

    elif mode == "color channels":
        if submode == "red channel":
            display_frame = frame.copy()
            display_frame[:, :, 0] = 0  # Zero out blue channel
            display_frame[:, :, 1] = 0  # Zero out green channel
        elif submode == "green channel":
            display_frame = frame.copy()
            display_frame[:, :, 0] = 0  # Zero out blue channel
            display_frame[:, :, 2] = 0  # Zero out red channel
        elif submode == "blue channel":
            display_frame = frame.copy()
            display_frame[:, :, 1] = 0  # Zero out green channel
            display_frame[:, :, 2] = 0  # Zero out red channel
        else:
            display_frame = frame
        display_frame = apply_trackbar_values(display_frame)
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
