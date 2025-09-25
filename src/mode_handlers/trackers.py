import cv2


class BrightnessTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.brightness = 50
        cv2.createTrackbar(
            "Brightness",
            self.window_name,
            self.brightness,
            100,
            self.on_brightness_change,
        )

    def on_brightness_change(self, value: int):
        self.brightness = value

    def get_brightness(self) -> int:
        return self.brightness


class ContrastTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.contrast = 50
        cv2.createTrackbar(
            "Contrast",
            self.window_name,
            self.contrast,
            100,
            self.on_contrast_change,
        )

    def on_contrast_change(self, value: int):
        self.contrast = value

    def get_contrast(self) -> int:
        return self.contrast


class KernelSizeTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.kernel_size = 1
        cv2.createTrackbar(
            "Kernel Size",
            self.window_name,
            self.kernel_size,
            20,
            self.on_kernel_size_change,
        )

    def on_kernel_size_change(self, value: int):
        self.kernel_size = value if value % 2 != 0 else value + 1
        if self.kernel_size < 1:
            self.kernel_size = 1

    def get_kernel_size(self) -> int:
        return self.kernel_size

    def get_effective_kernel_size(self) -> int:
        if self.kernel_size < 3:
            return 3
        elif self.kernel_size % 2 != 0:
            return self.kernel_size
        else:
            return self.kernel_size + 1


class SigmaTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.sigma = 1
        cv2.createTrackbar(
            "Sigma",
            self.window_name,
            self.sigma,
            20,
            self.on_sigma_change,
        )

    def on_sigma_change(self, value: int):
        self.sigma = max(1, value)

    def get_sigma(self) -> int:
        return self.sigma


class BilateralSigmaTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.sigma_color = 75
        self.sigma_space = 75
        cv2.createTrackbar(
            "Bilateral Sigma Color",
            self.window_name,
            self.sigma_color,
            200,
            self.on_sigma_color_change,
        )
        cv2.createTrackbar(
            "Bilateral Sigma Space",
            self.window_name,
            self.sigma_space,
            200,
            self.on_sigma_space_change,
        )

    def on_sigma_color_change(self, value: int):
        self.sigma_color = max(1, value)

    def on_sigma_space_change(self, value: int):
        self.sigma_space = max(1, value)

    def get_sigma_color(self) -> int:
        return self.sigma_color

    def get_sigma_space(self) -> int:
        return self.sigma_space


class CannyThresholdTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.threshold1 = 100
        self.threshold2 = 200
        cv2.createTrackbar(
            "Canny Threshold1",
            self.window_name,
            self.threshold1,
            255,
            self.on_threshold1_change,
        )
        cv2.createTrackbar(
            "Canny Threshold2",
            self.window_name,
            self.threshold2,
            255,
            self.on_threshold2_change,
        )

    def on_threshold1_change(self, value: int):
        self.threshold1 = max(1, value)

    def on_threshold2_change(self, value: int):
        self.threshold2 = max(1, value)

    def get_thresholds(self) -> tuple[int, int]:
        return self.threshold1, self.threshold2


class KernelSize3579Tracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.kernel_size = 3
        cv2.createTrackbar(
            "Kernel Size (3,5,7,9)",
            self.window_name,
            0,
            3,
            self.on_kernel_size_change,
        )

    def on_kernel_size_change(self, value: int):
        if value == 0:
            self.kernel_size = 3
        elif value == 1:
            self.kernel_size = 5
        elif value == 2:
            self.kernel_size = 7
        elif value == 3:
            self.kernel_size = 9

    def get_kernel_size(self) -> int:
        return self.kernel_size


class IntensityThresholdTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.threshold = 128
        cv2.createTrackbar(
            "Intensity Threshold",
            self.window_name,
            self.threshold,
            255,
            self.on_threshold_change,
        )

    def on_threshold_change(self, value: int):
        self.threshold = max(0, min(255, value))

    def get_threshold(self) -> int:
        return self.threshold


class HarrisParamsTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.block_size = 5
        self.sobel_ksize = 5
        self.dilate_ksize = 5
        self.threshold = 10
        cv2.createTrackbar(
            "Harris Block Size (3,5,7,9)",
            self.window_name,
            0,
            3,
            self.on_block_size_change,
        )
        cv2.createTrackbar(
            "Sobel Kernel Size (3,5,7,9)",
            self.window_name,
            0,
            3,
            self.on_sobel_ksize_change,
        )
        cv2.createTrackbar(
            "Dilate Kernel Size (3,5,7,9)",
            self.window_name,
            0,
            3,
            self.on_dilate_ksize_change,
        )
        cv2.createTrackbar(
            "Threshold (0.01 to 0.2)",
            self.window_name,
            self.threshold,
            20,
            self.on_threshold_change,
        )

    def on_block_size_change(self, value: int):
        if value == 0:
            self.block_size = 3
        elif value == 1:
            self.block_size = 5
        elif value == 2:
            self.block_size = 7
        elif value == 3:
            self.block_size = 9

    def on_sobel_ksize_change(self, value: int):
        if value == 0:
            self.sobel_ksize = 3
        elif value == 1:
            self.sobel_ksize = 5
        elif value == 2:
            self.sobel_ksize = 7
        elif value == 3:
            self.sobel_ksize = 9

    def on_dilate_ksize_change(self, value: int):
        if value == 0:
            self.dilate_ksize = 3
        elif value == 1:
            self.dilate_ksize = 5
        elif value == 2:
            self.dilate_ksize = 7
        elif value == 3:
            self.dilate_ksize = 9

    def on_threshold_change(self, value: int):
        self.threshold = max(1, min(20, value))

    def get_block_size(self) -> int:
        return self.block_size

    def get_sobel_ksize(self) -> int:
        return self.sobel_ksize

    def get_dilate_ksize(self) -> int:
        return self.dilate_ksize

    def get_threshold(self) -> float:
        return self.threshold / 100.0


class HoughLinesParamsTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.hough_threshold = 100
        cv2.createTrackbar(
            "Threshold (1-500)",
            self.window_name,
            self.hough_threshold,
            500,
            self.on_threshold_change,
        )

    def on_threshold_change(self, value: int):
        self.hough_threshold = max(1, value)

    def get_threshold(self) -> int:
        return self.hough_threshold


class HoughCirclesParamsTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.dp = 2
        self.min_dist = 500
        self.param1 = 200  # Canny high threshold
        self.param2 = 50  # Accumulator threshold
        self.min_radius = 0
        self.max_radius = 0
        cv2.createTrackbar(
            "dp (1-3)",
            self.window_name,
            self.dp,
            3,
            self.on_dp_change,
        )
        cv2.createTrackbar(
            "Min Dist (1-1000)",
            self.window_name,
            self.min_dist,
            1000,
            self.on_min_dist_change,
        )
        cv2.createTrackbar(
            "Param1 (1-255)",
            self.window_name,
            self.param1,
            255,
            self.on_param1_change,
        )
        cv2.createTrackbar(
            "Param2 (1-100)",
            self.window_name,
            self.param2,
            100,
            self.on_param2_change,
        )
        cv2.createTrackbar(
            "Min Radius (0-100)",
            self.window_name,
            self.min_radius,
            100,
            self.on_min_radius_change,
        )
        cv2.createTrackbar(
            "Max Radius (0-100)",
            self.window_name,
            self.max_radius,
            100,
            self.on_max_radius_change,
        )

    def on_dp_change(self, value: int):
        self.dp = max(1, value)

    def on_min_dist_change(self, value: int):
        self.min_dist = max(1, value)

    def on_param1_change(self, value: int):
        self.param1 = max(1, value)

    def on_param2_change(self, value: int):
        self.param2 = max(1, value)

    def on_min_radius_change(self, value: int):
        self.min_radius = max(0, value)

    def on_max_radius_change(self, value: int):
        self.max_radius = max(0, value)


class TranslateTracker:
    def __init__(self, window_name: str):
        self.window_name = window_name
        self.translate_x = 0
        self.translate_y = 0
        self.rotate_angle = 0
        self.scale_factor = 100  # 100 = 1.0x scale

        cv2.createTrackbar(
            "Translate X (-200 to 200)",
            self.window_name,
            200,  # Center position (0 offset)
            400,
            self.on_translate_x_change,
        )
        cv2.createTrackbar(
            "Translate Y (-200 to 200)",
            self.window_name,
            200,  # Center position (0 offset)
            400,
            self.on_translate_y_change,
        )
        cv2.createTrackbar(
            "Rotate Angle (0-360)",
            self.window_name,
            self.rotate_angle,
            360,
            self.on_rotate_change,
        )
        cv2.createTrackbar(
            "Scale (50-200%)",
            self.window_name,
            self.scale_factor,
            200,
            self.on_scale_change,
        )

    def on_translate_x_change(self, value: int):
        self.translate_x = value - 200  # Convert to -200 to 200 range

    def on_translate_y_change(self, value: int):
        self.translate_y = value - 200  # Convert to -200 to 200 range

    def on_rotate_change(self, value: int):
        self.rotate_angle = value

    def on_scale_change(self, value: int):
        self.scale_factor = max(50, value)

    def get_translate_x(self) -> int:
        return self.translate_x

    def get_translate_y(self) -> int:
        return self.translate_y

    def get_rotate_angle(self) -> int:
        return self.rotate_angle

    def get_scale_factor(self) -> float:
        return self.scale_factor / 100.0
