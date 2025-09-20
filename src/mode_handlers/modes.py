from mode_handlers.blur_sharpen import (
    AverageBlurHandler,
    BilateralBlurHandler,
    GaussianBlurAutoHandler,
    GaussianBlurHandler,
    MedianBlurHandler,
    SharpenHandler,
)
from mode_handlers.color_channels import (
    BlueChannelHandler,
    ColorChannelsHandler,
    GrayScaleHandler,
    GreenChannelHandler,
    RedChannelHandler,
)
from mode_handlers.corner import CornerDetectionHandler
from mode_handlers.edges import (
    CannyHandler,
    EdgeDetectionHandler,
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
    MorphologicalHandler,
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
    TransformationHandler,
)

keys2modes = {
    "1": "Default",
    "2": "Color Channels",
    "3": "Transformations",
    "4": "Blur and Sharpen",
    "5": "Edge Detection",
    "6": "Morphological Operations",
    "7": "Corner Detection and Hough Transform",
    "8": "SIFT and image stitching",
    "9": "Camera Calibration",
}

modes2keys = {v.lower(): k for k, v in keys2modes.items()}

mode_map = {
    "1": {
        "name": "Default",
        "submodes": {},
    },
    "2": {
        "name": "Color Channels",
        "submodes": {
            "q": {"name": "Default", "handler": ColorChannelsHandler},
            "w": {"name": "Red channel", "handler": RedChannelHandler},
            "e": {"name": "Green channel", "handler": GreenChannelHandler},
            "r": {"name": "Blue channel", "handler": BlueChannelHandler},
            "t": {"name": "Gray scale", "handler": GrayScaleHandler},
        },
    },
    "3": {
        "name": "Transformations",
        "submodes": {
            "q": {"name": "Default", "handler": TransformationHandler},
            "w": {"name": "Logarithmic", "handler": LogarithmicHandler},
            "e": {"name": "Exponential", "handler": ExponentialHandler},
            "r": {"name": "Power-law", "handler": PowerLawHandler},
            "t": {"name": "Thresholding", "handler": ThresholdingHandler},
            "y": {"name": "Negative", "handler": NegativeHandler},
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
            "q": {"name": "Default", "handler": EdgeDetectionHandler},
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
            "y": {"name": "Canny", "handler": CannyHandler},
        },
    },
    "6": {
        "name": "Morphological Operations",
        "submodes": {
            "q": {"name": "Default", "handler": MorphologicalHandler},
            "w": {"name": "Erosion", "handler": ErosionHandler},
            "e": {"name": "Dilation", "handler": DilationHandler},
            "r": {"name": "Opening", "handler": OpeningHandler},
            "t": {"name": "Closing", "handler": ClosingHandler},
            "y": {"name": "Morphological Gradient", "handler": MorphologicalGradientHandler},
            "u": {"name": "Top Hat", "handler": TopHatHandler},
            "i": {"name": "Black Hat", "handler": BlackHatHandler},
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
    "8": {  # Panorama
        "name": "SIFT and image stitching",
        "submodes": {
            "q": {"name": "Panorama", "handler": PanoramaHandler},
        },
    },
    "9": {  # T-Rex 3D
        "name": "Camera Calibration",
        "submodes": {},
    },
}
