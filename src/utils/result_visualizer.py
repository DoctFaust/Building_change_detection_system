import cv2
import numpy as np
import matplotlib.pyplot as plt

class ResultVisualizer:
    def create_change_visualization(self, change_map):
        """
        Create a color-coded change visualization
        
        Args:
            change_map (numpy.ndarray): Binary change detection map
        
        Returns:
            numpy.ndarray: Color-coded change visualization
        """
        color_map = np.zeros((*change_map.shape, 3), dtype=np.uint8)
        color_map[change_map == 0] = [0, 255, 0] 
        color_map[change_map == 1] = [255, 0, 0] 
        
        return color_map