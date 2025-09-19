from mode_handlers.blur_sharpen import BlurSharpenHandler
from mode_handlers.color_channels import ColorChannelsHandler
from mode_handlers.transformation import TransformationHandler

keys2modes = {
    "1": "Default",
    "2": "Color Channels",
    "3": "Transformations",
    "4": "Blur and Sharpen",
    "5": "Edge Detection",
    "6": "Morphological Operations",
    "7": "Corner Detection",
    "8": "Hough Transform",
    "9": "SIFT and image stitching",
    "10": "Camera Calibration",
}

modes2keys = {v.lower(): k for k, v in keys2modes.items()}

mode_map = {
    "1": {
        "name": "Default",
        "handler_class": None,
        "submodes": {},
    },
    "2": {
        "name": "Color Channels",
        "handler_class": ColorChannelsHandler,
        "submodes": {
            "q": "Default",
            "w": "Red channel",
            "e": "Green channel",
            "r": "Blue channel",
            "t": "Gray scale",
        },
    },
    "3": {
        "name": "Transformations",
        "handler_class": TransformationHandler,
        "submodes": {
            "q": "Default",
            "w": "Logarithmic",
            "e": "Exponential",
            "r": "Power-law",
            "t": "Thresholding",
            "y": "Negative",
        },
    },
    "4": {
        "name": "Blur and Sharpen",
        "handler_class": BlurSharpenHandler,
        "submodes": {
            "q": "Default",
            "w": "Averaging",
            "e": "Gaussian",
            "r": "Median",
            "t": "Bilateral",
            "y": "Sharpening",
        },
    },
    "5": {
        "name": "Edge Detection",
        "handler_class": None,
        "submodes": {
            "q": "Default",
            "w": "Robert",
            "e": "Prewitt",
            "r": "Sobel X",
            "t": "Sobel Y",
            "y": "Sobel XY",
            "u": "Laplacian",
            "i": "Canny",
        },
    },
    "6": {
        "name": "Morphological Operations",
        "handler_class": None,
        "submodes": {
            "q": "Default",
            "w": "Erosion",
            "e": "Dilation",
            "r": "Opening",
            "t": "Closing",
            "y": "Morphological Gradient",
            "u": "Top Hat",
            "i": "Black Hat",
        },
    },
    "7": {
        "name": "Corner Detection",
        "handler_class": None,
        "submodes": {},  # use harris corner detection
    },
    "8": {
        "name": "Hough Transform",
        "handler_class": None,
        "submodes": {
            "q": "Default",
            "w": "Hough Lines",
            "e": "Hough Circles",
        },
    },
    "9": {  # Panorama
        "name": "SIFT and image stitching",
        "handler_class": None,
        "submodes": {},
    },
    "10": {  # T-Rex 3D
        "name": "Camera Calibration",
        "handler_class": None,
        "submodes": {},
    },
}
