from mode_handlers.ar import ARHandler
from mode_handlers.blur_sharpen import (
    AverageBlurHandler,
    BilateralBlurHandler,
    GaussianBlurAutoHandler,
    GaussianBlurHandler,
    MedianBlurHandler,
    SharpenHandler,
)
from mode_handlers.camera_calibration import CameraCalibrationHandler
from mode_handlers.color_channels import (
    BlueChannelHandler,
    GrayScaleHandler,
    GreenChannelHandler,
    HSVHandler,
    RedChannelHandler,
    RGBHandler,
)
from mode_handlers.contrast_brightness import ContrastBrightnessHistogramHandler
from mode_handlers.corner import CornerDetectionHandler
from mode_handlers.edges import (
    CannyHandler,
    LaplacianHandler,
    PrewittXHandler,
    PrewittXYHandler,
    PrewittYHandler,
    RobertsXCrossHandler,
    RobertsXYCrossHandler,
    RobertsYCrossHandler,
    SobelHandler,
    SobelXHandler,
    SobelYHandler,
)
from mode_handlers.hough import HoughCirclesHandler, HoughLinesHandler
from mode_handlers.morph import (
    BlackHatHandler,
    ClosingHandler,
    DilationHandler,
    ErosionHandler,
    MorphologicalGradientHandler,
    OpeningHandler,
    TopHatHandler,
)
from mode_handlers.sift import PanoramaHandler
from mode_handlers.transformation import (
    ExponentialHandler,
    LogarithmicHandler,
    NegativeHandler,
    PowerLawHandler,
    ThresholdingHandler,
)
from mode_handlers.translate_rotate_scale import TranslateHandler

mode_map = {
    "1": {
        "name": "Color Channel",
        "submodes": {
            "q": {"name": "RGB", "handler": RGBHandler},
            "w": {"name": "Gray scale", "handler": GrayScaleHandler},
            "e": {"name": "HSV", "handler": HSVHandler},
            "r": {"name": "Red Channel", "handler": RedChannelHandler},
            "t": {"name": "Green Channel", "handler": GreenChannelHandler},
            "y": {"name": "Blue Channel", "handler": BlueChannelHandler},
        },
    },
    "2": {
        "name": "Contrast & Brightness & Histogram",
        "submodes": {
            "q": {"name": "Default", "handler": ContrastBrightnessHistogramHandler},
        },
    },
    "3": {
        "name": "Transformations",
        "submodes": {
            "q": {"name": "Logarithmic", "handler": LogarithmicHandler},
            "w": {"name": "Exponential", "handler": ExponentialHandler},
            "e": {"name": "Power-law", "handler": PowerLawHandler},
            "r": {"name": "Thresholding", "handler": ThresholdingHandler},
            "t": {"name": "Negative", "handler": NegativeHandler},
        },
    },
    "4": {
        "name": "Blur and Sharpen",
        "submodes": {
            "q": {"name": "Averaging", "handler": AverageBlurHandler},
            "w": {"name": "Gaussian", "handler": GaussianBlurHandler},
            "e": {"name": "GaussianAuto", "handler": GaussianBlurAutoHandler},
            "r": {"name": "Median", "handler": MedianBlurHandler},
            "t": {"name": "Bilateral", "handler": BilateralBlurHandler},
            "y": {"name": "Sharpening", "handler": SharpenHandler},
        },
    },
    "5": {
        "name": "Edge Detection",
        "submodes": {
            "q": {"name": "Canny", "handler": CannyHandler},
            "a": {"name": "Robert X", "handler": RobertsXCrossHandler},
            "s": {"name": "Robert Y", "handler": RobertsYCrossHandler},
            "d": {"name": "Robert XY", "handler": RobertsXYCrossHandler},
            "z": {"name": "Prewitt X", "handler": PrewittXHandler},
            "x": {"name": "Prewitt Y", "handler": PrewittYHandler},
            "c": {"name": "Prewitt XY", "handler": PrewittXYHandler},
            "w": {"name": "Sobel X", "handler": SobelXHandler},
            "e": {"name": "Sobel Y", "handler": SobelYHandler},
            "r": {"name": "Sobel XY", "handler": SobelHandler},
            "t": {"name": "Laplacian", "handler": LaplacianHandler},
        },
    },
    "6": {
        "name": "Morphological Operations",
        "submodes": {
            "q": {"name": "Erosion", "handler": ErosionHandler},
            "w": {"name": "Dilation", "handler": DilationHandler},
            "e": {"name": "Opening", "handler": OpeningHandler},
            "r": {"name": "Closing", "handler": ClosingHandler},
            "t": {"name": "Morphological Gradient", "handler": MorphologicalGradientHandler},
            "y": {"name": "Top Hat", "handler": TopHatHandler},
            "u": {"name": "Black Hat", "handler": BlackHatHandler},
        },
    },
    "7": {
        "name": "Corner Detection and Hough Transform",
        "submodes": {
            "q": {"name": "Harris Corner", "handler": CornerDetectionHandler},
            "w": {"name": "Hough Lines", "handler": HoughLinesHandler},
            "e": {"name": "Hough Circles", "handler": HoughCirclesHandler},
        },
    },
    "8": {
        "name": "Transform Image",
        "submodes": {
            "q": {"name": "Translate/Rotate/Scale", "handler": TranslateHandler},
        },
    },
    "9": {
        "name": "Panorama",
        "submodes": {
            "q": {"name": "Panorama", "handler": PanoramaHandler},
        },
    },
    "0": {
        "name": "Camera Calibration",
        "submodes": {
            "q": {"name": "Default", "handler": CameraCalibrationHandler},
        },
    },
    "-": {
        "name": "AR",
        "submodes": {
            "q": {"name": "Default", "handler": ARHandler},
        },
    },
}

keys2modes = {k: v["name"].lower() for k, v in mode_map.items()}

modes2keys = {v.lower(): k for k, v in keys2modes.items()}
