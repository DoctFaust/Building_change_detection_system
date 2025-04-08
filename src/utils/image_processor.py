import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        pass

    def preprocess(self, image_path, target_size=(256, 256)):
        """
        Preprocess image for change detection
        
        Args:
            image_path (str): Path to image file
            target_size (tuple): Desired output image size
        
        Returns:
            numpy.ndarray: Preprocessed image
        """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
        
        image = image.astype(np.float32) / 255.0
        
        return image