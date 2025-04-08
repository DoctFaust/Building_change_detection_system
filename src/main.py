import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.main_window import BuildingChangeDetectionApp
from PyQt5.QtGui import QIcon

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion') 
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "icons", "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    main_window = BuildingChangeDetectionApp()
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()