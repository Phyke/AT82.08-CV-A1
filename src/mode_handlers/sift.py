import cv2
import numpy as np
from cv2.typing import MatLike

from .base import BaseModeHandler


class PanoramaHandler(BaseModeHandler):
    def __init__(self):
        super().__init__()
        self.captured_images = []
        self.panorama = None  # Store stitched result
        self.stitch_error = False

    def setup_window(
        self,
        *args,
        **kwargs,
    ):
        super().setup_window(have_control_window=False, *args, **kwargs)
        cv2.namedWindow("Panorama Captures", cv2.WINDOW_AUTOSIZE)
        # main_window_width = kwargs.get("main_window_width", 640)
        # main_window_height = kwargs.get("main_window_height", 480)
        # cv2.resizeWindow("Panorama Captures", main_window_width, main_window_height)

    def process_frame(self, frame: MatLike) -> MatLike:
        # Show stitched panorama if available
        if self.panorama is not None:
            cv2.imshow("Panorama Captures", self.panorama)
        elif self.stitch_error:
            shape = frame.shape
            dtype = frame.dtype
            error_img = np.zeros(shape, dtype)
            cv2.putText(
                error_img,
                "Stitching failed",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                error_img,
                "Change angle and press capture again",
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
            cv2.imshow("Panorama Captures", error_img)
        else:
            empty_img = np.zeros_like(frame)
            cv2.imshow("Panorama Captures", empty_img)
        return frame

    def handle_key(self, key, frame: MatLike):
        if key == ord(" ") and len(self.captured_images) < 5:
            print("Captured image for panorama.")
            self.captured_images.append(frame.copy())
            # Stitch if at least 2 images
            if len(self.captured_images) >= 2:
                success, pano = self.stitch()
                if success:
                    self.panorama = pano
                    self.stitch_error = False
                else:
                    self.panorama = None
                    self.stitch_error = True

        elif key == ord("r"):
            print("Resetting captured images.")
            self.captured_images = []
            self.panorama = None
            self.stitch_error = False

    def stitch(self):
        sift = cv2.SIFT_create()
        grays = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in self.captured_images]
        keypoints = []
        descriptors = []
        for gray in grays:
            keypoint, descriptor = sift.detectAndCompute(gray, None)
            keypoints.append(keypoint)
            descriptors.append(descriptor)

        bf = cv2.BFMatcher()
        matches = []
        for i in range(len(descriptors) - 1):
            match = bf.knnMatch(descriptors[i], descriptors[i + 1], k=2)
            matches.append(match)

        good_matches = []
        for match in matches:
            good = []
            for m, n in match:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            good_matches.append(good)

        homographies = []
        for i in range(len(good_matches)):
            if len(good_matches[i]) < 4:
                print("Not enough matches to compute homography.")
                return False, None
            M = self.ransac_transform(keypoints[i], keypoints[i + 1], good_matches[i])
            if M is None:
                print("Homography computation failed.")
                return False, None
            homographies.append(M)

        images = self.captured_images
        n = len(images)

        h_left, w_left = images[-2].shape[:2]
        pano_width = w_left + images[-1].shape[1]
        pano_height = h_left
        pano = cv2.warpPerspective(images[-1], homographies[-1], (pano_width, pano_height))
        pano[:h_left, :w_left] = images[-2]

        for k in range(n - 3, -1, -1):
            h, w = images[k].shape[:2]
            pano_width = w + pano.shape[1]
            pano_height = h
            pano = cv2.warpPerspective(pano, homographies[k], (pano_width, pano_height))
            pano[:h, :w] = images[k]

        # If all pixels in a column are black, remove that column
        # Remove right-side black columns
        col_mask = np.all(pano == 0, axis=(0, 2))
        last_col = np.argmax(col_mask[::])
        if last_col > 0:
            pano = pano[:, :last_col]

        return True, pano

    def ransac_transform(self, kp1, kp2, matches):
        src_pts = np.zeros((len(matches), 2), dtype=np.float32)
        dst_pts = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            dst_pts[i, :] = kp1[match[0].queryIdx].pt
            src_pts[i, :] = kp2[match[0].trainIdx].pt

        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)
        return M
