# AT82.08-CV-A1
Computer Vision – Assignment 1 (Aug 2025)

## How to run
- Note: `cd src` is important because of relative paths
```bat
git clone https://github.com/Phyke/AT82.08-CV-A1.git
cd AT82.08-CV-A1
uv sync
cd src
python app.py
```

# Application Modes & Usage Instructions

## Controls
- Press keys `1`, `2`, `3`, ... to switch between modes.
- After selecting a mode, first submode is automatically selected.
- Press keys `q`, `w`, `e`, `r`, `t`, ... to switch between submodes within a mode.
- Press `ESC` to exit the application.
- Use trackbars to adjust parameters in applicable modes.

## Modes and Submodes

| Main Key | Mode Name                            | Submode Key(s) | Submode Name(s)        |
| -------- | ------------------------------------ | -------------- | ---------------------- |
| 1        | Color Channel                        | q              | RGB                    |
|          |                                      | w              | Gray scale             |
|          |                                      | e              | HSV                    |
|          |                                      | r              | Red Channel            |
|          |                                      | t              | Green Channel          |
|          |                                      | y              | Blue Channel           |
| 2        | Contrast & Brightness & Histogram    | q              | Main                   |
| 3        | Transformations                      | q              | Logarithmic            |
|          |                                      | w              | Exponential            |
|          |                                      | e              | Power-law              |
|          |                                      | r              | Thresholding           |
|          |                                      | t              | Negative               |
| 4        | Blur and Sharpen                     | q              | Averaging              |
|          |                                      | w              | Gaussian               |
|          |                                      | e              | GaussianAuto           |
|          |                                      | r              | Median                 |
|          |                                      | t              | Bilateral              |
|          |                                      | y              | Sharpening             |
| 5        | Edge Detection                       | q              | Canny                  |
|          |                                      | a              | Robert X               |
|          |                                      | s              | Robert Y               |
|          |                                      | d              | Robert XY              |
|          |                                      | z              | Prewitt X              |
|          |                                      | x              | Prewitt Y              |
|          |                                      | c              | Prewitt XY             |
|          |                                      | w              | Sobel X                |
|          |                                      | e              | Sobel Y                |
|          |                                      | r              | Sobel XY               |
|          |                                      | t              | Laplacian              |
| 6        | Morphological Operations             | q              | Erosion                |
|          |                                      | w              | Dilation               |
|          |                                      | e              | Opening                |
|          |                                      | r              | Closing                |
|          |                                      | t              | Morphological Gradient |
|          |                                      | y              | Top Hat                |
|          |                                      | u              | Black Hat              |
| 7        | Corner Detection and Hough Transform | q              | Harris Corner          |
|          |                                      | w              | Hough Lines            |
|          |                                      | e              | Hough Circles          |
| 8        | Transform Image                      | q              | Translate/Rotate/Scale |
| 9        | Panorama                             | q              | Panorama               |
| 0        | Camera Calibration                   | q              | Camera Calibration     |
| -        | AR                                   | q              | AR                     |

### Control References
1. Color Channel
    - No trackbars.

2. Contrast & Brightness & Histogram
   - Contrast: (0 – 100 mapped to 0.0 - 2.0)
   - Brightness: (0 – 100 mapped to −50 - +50)

3. Transformations
   - No trackbars (fixed parameters for all submodes).

4. Blur and Sharpen
   - Averaging:
     - Kernel Size ≥ 3, force odd number
   - Gaussian:
     - Kernel Size ≥ 3, force odd number
     - Sigma (1–20)
   - GaussianAuto:
     - Sigma (1–20)
     - Kernel is automatically computed as k = ceil(2πσ), also force odd number ≥ 3
   - Median:
     - Kernel Size ≥ 3, force odd number
   - Bilateral:
     - Kernel Size ≥ 3, force odd number (as d)
     - Sigma Color (1–200)
     - Sigma Space (1–200).
   - Sharpening:
     - No sliders (fixed 3×3 kernel).

5. Edge Detection
   - Canny:
     - Threshold1 (1–255)
     - Threshold2 (1–255).
   - Roberts / Prewitt / Sobel / Laplacian:
     - No sliders (fixed kernels/defaults).

6. Morphological Operations
   - Erosion / Dilation / Opening / Closing / Morph Gradient / Top Hat / Black Hat:
     - All submodes apply binarizing using Intensity Threshold (0–255).
     - Kernel Size (3,5,7,9).

7. Corner Detection and Hough Transform
   - Harris Corner:
     - Block Size (3,5,7,9)
     - Sobel ksize (3,5,7,9)
     - Dilate ksize (3,5,7,9)
     - Threshold (1–20 mapped to 0.01–0.20).
   - Hough Lines:
     - Canny Threshold1 (1–255)
     - Canny Threshold2 (1–255).
     - Hough Threshold (raw 1–500; used directly).
   - Hough Circles:
     - dp (1–3)
     - MinDist (1–1000)
     - Param1 (1–255)
     - Param2 (1–100)
     - Min/Max Radius (0–100; 0 = auto).
     - Internally applies median blur k=5 otherwise my camera don't work well somehow.

8. Transform Image — Translate/Rotate/Scale
   - Translate/Rotate/Scale
     - X/Y: 0–400 mapped to −200 - 200 (centered at 200)
     - Angle: 0–360
     - Scale: 50–200 mapped to (0.5×..2.0×)

9. Panorama
   - No sliders.
   - SPACE to capture (up to 5)
   - r to reset.
   - A new window previews stitched results.

10. Camera Calibration
    - No sliders.
    - Use a 9×6 chessboard (`assets/A4_Chessboard_9x6.png`).
    - 20 images are auto‑captured then calibrated and saved to `assets/calibration.npz`.
    - I used my iPad for displaying the chessboard pattern so I changed the `SQUARE_SIZE_MM` in the code to `20`.

11. AR
    - No sliders.
    - Requires `assets/calibration.npz`.

## Total hours spent
~2 + ~4 + ~5.5 + ~7 + ~5 + ~1.5 = ~25 hours
