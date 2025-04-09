import cv2
import numpy as np
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QFont, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QSize, QRect
import os

class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px dashed #dadce0;
                border-radius: 6px;
                color: #5f6368;
            }
        """)
        
        self.setText("无图像")
        self.setFont(QFont("Times New Roman", 12))
        
        self.setMinimumSize(400, 400) 
        self.current_image = None
        self.zoom_level = 1.0
        self.fit_to_view = True
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_image is not None:
            self._update_display()

    def load_image(self, image_path):
        try:
            if isinstance(image_path, str):
                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"Image file not found: {image_path}")
                
                _, ext = os.path.splitext(image_path)
                ext = ext.lower()
                
                if ext in ['.tif', '.tiff']:
                    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                    
                    if len(image.shape) > 2 and image.shape[2] > 3:
                        image = image[:, :, :3]
                    
                    if image.dtype != np.uint8:
                        if image.max() > 0:
                            image = (image / image.max() * 255).astype(np.uint8)
                        else:
                            image = np.zeros_like(image, dtype=np.uint8)
                    
                    if len(image.shape) == 3 and image.shape[2] == 3:
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    elif len(image.shape) == 2:  
                        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                
                else: 
                    image = cv2.imread(image_path)
                    if image is None:
                        raise ValueError(f"Failed to read image: {image_path}")
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image = image_path.copy()
            
            self.current_image = image
            self.zoom_level = 1.0
            self.fit_to_view = True
            
            self._update_display()
            
        except Exception as e:
            print(f"Error in load_image: {str(e)}")
            self.clear()
            self.setText(f"Error loading image: {str(e)}")
            raise
    
    def _update_display(self):
        if self.current_image is None:
            return
        
        try:
            h, w = self.current_image.shape[:2]
            
            if len(self.current_image.shape) == 2:
                ch = 1
                qt_format = QImage.Format_Grayscale8
                data = self.current_image.tobytes()
                bytes_per_line = w
            elif self.current_image.shape[2] == 3:
                ch = 3
                qt_format = QImage.Format_RGB888
                data = self.current_image.data.tobytes()
                bytes_per_line = ch * w
            elif self.current_image.shape[2] == 4:
                ch = 4
                qt_format = QImage.Format_RGBA8888
                data = self.current_image.data.tobytes()
                bytes_per_line = ch * w
            else:
                raise ValueError(f"Unsupported image format with {self.current_image.shape[2]} channels")
            
            qt_image = QImage(data, w, h, bytes_per_line, qt_format)
            pixmap = QPixmap.fromImage(qt_image)
            
            if self.fit_to_view:
                scaled_pixmap = pixmap.scaled(
                    self.width() - 10, 
                    self.height() - 10, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
            else:
                scaled_w = int(w * self.zoom_level)
                scaled_h = int(h * self.zoom_level)
                scaled_pixmap = pixmap.scaled(
                    scaled_w,
                    scaled_h,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            
            self.setPixmap(scaled_pixmap)
            
        except Exception as e:
            print(f"Error in _update_display: {str(e)}")
            self.clear()
            self.setText(f"Error displaying image: {str(e)}")
            raise
    
    def wheelEvent(self, event):
        if self.current_image is not None:
            delta = event.angleDelta().y()
            
            if delta > 0:
                self.zoom_level *= 1.1 
            else:
                self.zoom_level *= 0.9 
                
            self.zoom_level = max(0.1, min(5.0, self.zoom_level))
            
            self.fit_to_view = False
            
            self._update_display()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton and self.current_image is not None:
            self.zoom_level = 1.0
            self.fit_to_view = True
            self._update_display()