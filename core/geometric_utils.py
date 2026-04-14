from typing import Dict, List
import math

class GeometricEngine:
    """
    Advanced mathematical computations for Revit geometry.
    Handles distance vectors, clearing calculations, and spatial validations.
    """

    @staticmethod
    def calculate_diagonal(bounding_box: Dict[str, List[float]]) -> float:
        """ Calculates the 3D clear diagonal of an element's bounding box. """
        if not bounding_box or "min" not in bounding_box or "max" not in bounding_box:
            return 0.0
            
        min_pt = bounding_box["min"]
        max_pt = bounding_box["max"]
        
        dx = max_pt[0] - min_pt[0]
        dy = max_pt[1] - min_pt[1]
        dz = max_pt[2] - min_pt[2]
        
        return math.sqrt(dx**2 + dy**2 + dz**2)

    @staticmethod
    def get_clear_width(bounding_box: Dict[str, List[float]]) -> float:
        """ Evaluates the clear usable width (e.g. for a door or corridor). """
        if not bounding_box or "min" not in bounding_box or "max" not in bounding_box:
            return 0.0
            
        min_pt = bounding_box["min"]
        max_pt = bounding_box["max"]
        
        dx = abs(max_pt[0] - min_pt[0])
        dy = abs(max_pt[1] - min_pt[1])
        
        # Typically the smaller planar dimension is thickness, larger is width
        return max(dx, dy)
