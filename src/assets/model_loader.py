"""
3D Model Loader for OBJ files
Loads and processes 3D models for AR rendering
"""

import numpy as np
from typing import List, Tuple, Optional
import cv2

class OBJLoader:
    """Loads and manages 3D models from OBJ files"""
    
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.edges = []
        
    def load_obj(self, file_path: str, scale: float = 1.0) -> bool:
        """
        Load OBJ file and extract vertices and faces
        
        Args:
            file_path: Path to the OBJ file
            scale: Scale factor to resize the model
            
        Returns:
            bool: True if loaded successfully
        """
        try:
            self.vertices = []
            self.faces = []
            
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    
                    # Parse vertices (v x y z)
                    if line.startswith('v '):
                        parts = line.split()
                        if len(parts) >= 4:
                            x = float(parts[1]) * scale
                            y = float(parts[2]) * scale
                            z = float(parts[3]) * scale
                            self.vertices.append([x, y, z])
                    
                    # Parse faces (f v1 v2 v3 or f v1/t1/n1 v2/t2/n2 v3/t3/n3)
                    elif line.startswith('f '):
                        parts = line.split()
                        if len(parts) >= 4:
                            # Extract vertex indices (1-based in OBJ, convert to 0-based)
                            face_vertices = []
                            for i in range(1, len(parts)):
                                # Handle both "v" and "v/t/n" formats
                                vertex_data = parts[i].split('/')
                                vertex_idx = int(vertex_data[0]) - 1  # Convert to 0-based
                                face_vertices.append(vertex_idx)
                            
                            # Triangulate if more than 3 vertices (simple fan triangulation)
                            for i in range(1, len(face_vertices) - 1):
                                triangle = [
                                    face_vertices[0],
                                    face_vertices[i],
                                    face_vertices[i + 1]
                                ]
                                self.faces.append(triangle)
            
            self.vertices = np.array(self.vertices, dtype=np.float32)
            self._generate_edges()
            
            print(f"Loaded OBJ: {len(self.vertices)} vertices, {len(self.faces)} faces")
            return len(self.vertices) > 0
            
        except Exception as e:
            print(f"Error loading OBJ file: {e}")
            return False
    
    def _generate_edges(self):
        """Generate edge list from faces for wireframe rendering"""
        edge_set = set()
        
        for face in self.faces:
            # Add edges for each triangle
            for i in range(len(face)):
                v1 = face[i]
                v2 = face[(i + 1) % len(face)]
                # Store edge in consistent order (smaller index first)
                edge = tuple(sorted([v1, v2]))
                edge_set.add(edge)
        
        self.edges = list(edge_set)
    
    def get_vertices(self) -> np.ndarray:
        """Get model vertices"""
        return self.vertices.copy()
    
    def get_faces(self) -> List[List[int]]:
        """Get model faces"""
        return self.faces.copy()
    
    def get_edges(self) -> List[Tuple[int, int]]:
        """Get model edges for wireframe rendering"""
        return self.edges.copy()
    
    def get_bounding_box(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get model bounding box
        
        Returns:
            Tuple of (min_coords, max_coords)
        """
        if len(self.vertices) == 0:
            return np.zeros(3), np.zeros(3)
        
        min_coords = np.min(self.vertices, axis=0)
        max_coords = np.max(self.vertices, axis=0)
        
        return min_coords, max_coords
    
    def center_model(self):
        """Center the model at origin"""
        if len(self.vertices) > 0:
            min_coords, max_coords = self.get_bounding_box()
            center = (min_coords + max_coords) / 2
            self.vertices -= center
    
    def scale_model(self, target_size: float):
        """
        Scale model to fit within target_size
        
        Args:
            target_size: Maximum dimension size
        """
        if len(self.vertices) > 0:
            min_coords, max_coords = self.get_bounding_box()
            current_size = np.max(max_coords - min_coords)
            
            if current_size > 0:
                scale_factor = target_size / current_size
                self.vertices *= scale_factor


class Model3D:
    """3D Model representation for AR rendering"""
    
    def __init__(self, obj_loader: OBJLoader):
        self.obj_loader = obj_loader
        self.position = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])  # Euler angles in degrees
        self.scale = 1.0
        
    def set_position(self, x: float, y: float, z: float):
        """Set model position"""
        self.position = np.array([x, y, z])
    
    def set_rotation(self, rx: float, ry: float, rz: float):
        """Set model rotation (degrees)"""
        self.rotation = np.array([rx, ry, rz])
    
    def set_scale(self, scale: float):
        """Set model scale"""
        self.scale = scale
    
    def get_transformed_vertices(self) -> np.ndarray:
        """
        Get vertices with current transformation applied
        
        Returns:
            Transformed vertices as Nx3 array
        """
        vertices = self.obj_loader.get_vertices() * self.scale
        
        # Apply rotation (ZYX order)
        rx, ry, rz = np.radians(self.rotation)
        
        # Rotation matrices
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(rx), -np.sin(rx)],
            [0, np.sin(rx), np.cos(rx)]
        ])
        
        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry)],
            [0, 1, 0],
            [-np.sin(ry), 0, np.cos(ry)]
        ])
        
        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0],
            [np.sin(rz), np.cos(rz), 0],
            [0, 0, 1]
        ])
        
        # Combined rotation
        R = Rz @ Ry @ Rx
        
        # Apply rotation
        rotated_vertices = vertices @ R.T
        
        # Apply translation
        transformed_vertices = rotated_vertices + self.position
        
        return transformed_vertices
    
    def get_edges(self) -> List[Tuple[int, int]]:
        """Get model edges"""
        return self.obj_loader.get_edges()
    
    def get_faces(self) -> List[List[int]]:
        """Get model faces"""
        return self.obj_loader.get_faces()
