import os

import cv2
import numpy as np

from .base import BaseModeHandler


class ARHandler(BaseModeHandler):
    def __init__(self):
        # --- AR & Pinhole Explorer State ---
        self.mtx = np.eye(3)
        self.dist = np.zeros((1, 5))
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.aruco_detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        self._load_calibration()
        self.pinhole_params = {"fx": self.mtx[0, 0], "fy": self.mtx[1, 1], "cx": self.mtx[0, 2], "cy": self.mtx[1, 2]}
        self.load_model()

    def load_model(self):
        obj_path = os.path.join("assets", "trex_model.obj")
        self.trex_vertices = []
        self.trex_faces = []
        if os.path.exists(obj_path):
            with open(obj_path, "r") as f:
                for line in f:
                    if line.startswith("v "):  # vertex
                        parts = line.strip().split()
                        vertex = parts[1:4]
                        self.trex_vertices.append(vertex)
                    elif line.startswith("f "):  # face
                        parts = line.strip().split()[1:]
                        # Face indices (OBJ is 1-based, so subtract 1)
                        face = [int(p.split("/")[0]) - 1 for p in parts]
                        self.trex_faces.append(face)
            self.trex_vertices = np.array(self.trex_vertices, dtype=np.float32) * 0.0005
            center = np.mean(self.trex_vertices, axis=0)
            self.trex_vertices -= center
            self.trex_faces = np.array(self.trex_faces, dtype=np.int32)

            print(f"Loaded {len(self.trex_vertices)} vertices and {len(self.trex_faces)} faces from {obj_path}.")
        else:
            print(f"Model file not found: {obj_path}")

    def _load_calibration(self):
        if os.path.exists("assets/calibration.npz"):
            with np.load("assets/calibration.npz") as X:
                self.mtx, self.dist = [X[i] for i in ("mtx", "dist")]
            print("Calibration data loaded.")
        else:
            print("WARNING: 'calibration.npz' not found. AR and Pinhole modes will not be accurate.")

    def process_frame(self, frame):
        return self._draw_ar_mode(frame)

    def _draw_trex(self, frame, camera_matrix):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.aruco_detector.detectMarkers(gray)

        if ids is not None:
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, self.dist)

            # Project all vertices at once
            vertices = self.trex_vertices.reshape(-1, 3)
            print(f"Projecting {len(vertices)} vertices.")
            img_pts, _ = cv2.projectPoints(vertices, rvecs[0], tvecs[0], camera_matrix, self.dist)
            img_pts = img_pts.reshape(-1, 2).astype(int)

            # Draw each face as polyline
            for face in self.trex_faces:
                pts = img_pts[face]  # select the projected vertices for this face
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=1)

            print(f"Drew {len(self.trex_faces)} faces of the T-Rex model.")
        else:
            # print("No ArUco markers detected.")
            cv2.putText(frame, "No ArUco markers detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        frame = cv2.flip(frame, 1)  # Flip once at end
        return frame

    def _draw_ar_cube(self, frame, camera_matrix):
        # --- AR & Pinhole Implementations---
        # frame = cv2.flip(frame, 1)  # This cause a bug for some reason
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.aruco_detector.detectMarkers(gray)
        if ids is not None:
            print(f"Detected ArUco markers: {ids.flatten()}")
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, self.dist)
            axis_len = 0.05
            obj_pts = np.float32(
                [
                    [0, 0, 0],
                    [axis_len, 0, 0],
                    [axis_len, axis_len, 0],
                    [0, axis_len, 0],
                    [0, 0, -axis_len],
                    [axis_len, 0, -axis_len],
                    [axis_len, axis_len, -axis_len],
                    [0, axis_len, -axis_len],
                ]
            )
            img_pts, _ = cv2.projectPoints(obj_pts, rvecs[0], tvecs[0], camera_matrix, self.dist)
            img_pts = np.int32(img_pts).reshape(-1, 2)
            # Define cube faces by indices
            faces = [
                [0, 1, 2, 3],  # bottom
                [4, 5, 6, 7],  # top
                [0, 1, 5, 4],  # side 1
                [1, 2, 6, 5],  # side 2
                [2, 3, 7, 6],  # side 3
                [3, 0, 4, 7],  # side 4
            ]
            face_colors = [
                (255, 0, 0),  # Blue
                (0, 255, 0),  # Green
                (0, 0, 255),  # Red
                (255, 255, 0),  # Cyan
                (255, 0, 255),  # Magenta
                (0, 255, 255),  # Yellow
            ]
            # Draw filled faces
            for idx, face in enumerate(faces):
                cv2.fillConvexPoly(frame, img_pts[face], face_colors[idx], lineType=cv2.LINE_AA)
            # Draw black wireframe
            for face in faces:
                cv2.polylines(frame, [img_pts[face]], isClosed=True, color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
        else:
            print("No ArUco markers detected.")
            cv2.putText(frame, "No ArUco markers detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        frame = cv2.flip(frame, 1)  # Flip only once at the end for display
        return frame

    def _draw_ar_mode(self, frame):
        return self._draw_trex(frame, self.mtx)
