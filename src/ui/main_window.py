import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QTabWidget, 
                             QMessageBox, QProgressBar, QSplitter, QGroupBox,
                             QLineEdit, QFrame, QStatusBar, QComboBox, QFormLayout)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QDir

from .image_viewer import ImageViewer
from models.predict import predict_changes

class BuildingChangeDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_dir = os.path.dirname(os.path.dirname(sys.executable))
        self.output_dir = os.path.join(self.app_dir, "result")
        self.default_model_path = os.path.join(self.app_dir, "model", "model.pth")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.initUI()
        
        self.image_paths = {
            'before': None,
            'after': None
        }
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fefeea;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
            }
            QPushButton {
                background-color: #4b7bec;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3867d6;
            }
            QPushButton:disabled {
                background-color: #a5b1c2;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 6px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #e9e9e9;
                border: 1px solid #cccccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 6px 10px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                margin-bottom: -1px;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px;
                background-color: #ffffff;
            }
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px;
                background-color: #ffffff;
            }
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                text-align: center;
                background-color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #4b7bec;
            }
            QStatusBar {
                background-color: #4b7bec;
                color: #333333;
            }
        """)

    def initUI(self):
        self.setWindowTitle('多层次注意力残差UNet++模型建筑物变化检测系统')
        self.setGeometry(100, 100, 1200, 800)
        
        icon_dir = os.path.join(self.app_dir, "icon")
        
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setFixedWidth(300)
        
        image_group = QGroupBox("图像选择")
        image_layout = QVBoxLayout()
        image_group.setLayout(image_layout)
        
        before_layout = QHBoxLayout()
        self.before_btn = QPushButton('变化前图像')
        try:
            self.before_btn.setIcon(QIcon(os.path.join(icon_dir, "upload.png")))
        except:
            pass
        self.before_btn.clicked.connect(lambda: self.upload_image('before'))
        self.before_btn.setToolTip("请选择区域建筑物变化前的图像进行上传")
        before_layout.addWidget(self.before_btn)
        
        self.before_path_label = QLabel("未选择")
        self.before_path_label.setWordWrap(True)
        before_layout.addWidget(self.before_path_label)
        image_layout.addLayout(before_layout)
        
        after_layout = QHBoxLayout()
        self.after_btn = QPushButton('变化后图像')
        try:
            self.after_btn.setIcon(QIcon(os.path.join(icon_dir, "upload.png")))
        except:
            pass
        self.after_btn.clicked.connect(lambda: self.upload_image('after'))
        self.after_btn.setToolTip("请选择同一区域变化后的图像进行上传")
        after_layout.addWidget(self.after_btn)
        
        self.after_path_label = QLabel("未选择")
        self.after_path_label.setWordWrap(True)
        after_layout.addWidget(self.after_path_label)
        image_layout.addLayout(after_layout)
        
        left_layout.addWidget(image_group)
        
        model_group = QGroupBox("模型选择")
        model_layout = QVBoxLayout()
        model_group.setLayout(model_layout)
        
        model_type_layout = QFormLayout()
        self.model_type = QComboBox()
        self.model_type.addItem("默认模型", self.default_model_path)
        self.model_type.addItem("自定义模型", "")
        self.model_type.currentIndexChanged.connect(self.on_model_type_changed)
        model_type_layout.addRow("检测模型:", self.model_type)
        model_layout.addLayout(model_type_layout)
        
        model_path_layout = QHBoxLayout()
        self.model_path_edit = QLineEdit()
        self.model_path_edit.setEnabled(False)
        self.model_path_edit.setPlaceholderText("模型权重文件路径 (.pth)")
        model_path_layout.addWidget(self.model_path_edit)
        
        self.model_browse_btn = QPushButton("浏览...")
        try:
            self.model_browse_btn.setIcon(QIcon(os.path.join(icon_dir, "folder.png")))
        except:
            pass
        self.model_browse_btn.clicked.connect(self.browse_model)
        self.model_browse_btn.setEnabled(False)
        model_path_layout.addWidget(self.model_browse_btn)
        
        model_layout.addLayout(model_path_layout)
        left_layout.addWidget(model_group)
        
        analysis_group = QGroupBox("变化检测")
        analysis_layout = QVBoxLayout()
        analysis_group.setLayout(analysis_layout)
        
        self.analyze_btn = QPushButton('开始分析')
        try:
            self.analyze_btn.setIcon(QIcon(os.path.join(icon_dir, "analyze.png")))
        except:
            pass
        self.analyze_btn.clicked.connect(self.analyze_changes)
        self.analyze_btn.setEnabled(False)
        analysis_layout.addWidget(self.analyze_btn)
        
        progress_layout = QVBoxLayout()
        progress_layout.addWidget(QLabel("检测进度:"))
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        analysis_layout.addLayout(progress_layout)
        
        left_layout.addWidget(analysis_group)
        
        left_layout.addStretch()
        
        results_group = QGroupBox("检测结果")
        results_layout = QVBoxLayout()
        results_group.setLayout(results_layout)
        
        self.save_results_btn = QPushButton("保存变化图像")
        try:
            self.save_results_btn.setIcon(QIcon(os.path.join(icon_dir, "save.png")))
        except:
            pass
        self.save_results_btn.clicked.connect(self.save_results)
        self.save_results_btn.setEnabled(False)
        results_layout.addWidget(self.save_results_btn)
        
        left_layout.addWidget(results_group)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        self.image_viewers = QTabWidget()
        
        self.before_viewer = ImageViewer()
        self.image_viewers.addTab(self.before_viewer, '变化前图像')
        
        self.after_viewer = ImageViewer()
        self.image_viewers.addTab(self.after_viewer, '变化后图像')
        
        self.result_viewer = ImageViewer()
        self.image_viewers.addTab(self.result_viewer, '变化二值图')
        
        right_layout.addWidget(self.image_viewers)
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("准备就绪")

    def on_model_type_changed(self, index):
        if index == 0: 
            self.model_path_edit.setEnabled(False)
            self.model_browse_btn.setEnabled(False)
            self.model_path_edit.setText("")
        else: 
            self.model_path_edit.setEnabled(True)
            self.model_browse_btn.setEnabled(True)

    def browse_model(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Select Model Parameter File', 
            '', 
            'PyTorch 模型参数文件 (*.pth)'
        )
        
        if file_path:
            self.model_path_edit.setText(file_path)
            self.model_type.setItemData(1, file_path)

    def upload_image(self, image_type):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                f'Select {image_type.capitalize()} Image', 
                '', 
                'Image Files (*.tif *.tiff *.png *.jpg *.jpeg)'
            )
            
            if file_path:
                self.image_paths[image_type] = file_path
                
                path_label = self.before_path_label if image_type == 'before' else self.after_path_label
                file_name = os.path.basename(file_path)
                path_label.setText(file_name)
                path_label.setToolTip(file_path)
                
                viewer = self.before_viewer if image_type == 'before' else self.after_viewer
                viewer.load_image(file_path)
                
                self.analyze_btn.setEnabled(
                    self.image_paths['before'] is not None and 
                    self.image_paths['after'] is not None
                )
                
                self.image_viewers.setCurrentIndex(0 if image_type == 'before' else 1)
                
                self.statusBar.showMessage(f"{image_type.capitalize()} image loaded: {file_name}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to load image: {str(e)}")
            self.statusBar.showMessage(f"Error loading {image_type} image")

    def get_model_path(self):
        if self.model_type.currentIndex() == 0:
            return self.default_model_path
        else:
            custom_path = self.model_path_edit.text().strip()
            if not custom_path:
                QMessageBox.warning(self, "Warning", "请选择一个本地模型参数文件.")
                return None
            if not os.path.exists(custom_path):
                QMessageBox.warning(self, "Warning", "选择的模型文件不存在")
                return None
            return custom_path

    def analyze_changes(self):
        try:
            if not all(self.image_paths.values()):
                QMessageBox.warning(self, 'Error', '请上传变化前后图像')
                return
            
            model_path = self.get_model_path()
            if not model_path:
                return
                
            self.statusBar.showMessage("检测中...")
            self.progress_bar.setValue(0)
            self.progress_bar.setMaximum(0) 
            
            output_path = os.path.join(self.output_dir, "result_image.png")
            
            try:
                result_image = predict_changes(
                    self.image_paths['before'], 
                    self.image_paths['after'],
                    model_path=model_path,
                    output_path=output_path
                )
                
                self.result_viewer.load_image(output_path)
                self.image_viewers.setCurrentIndex(2)
                self.save_results_btn.setEnabled(True)
                
                self.statusBar.showMessage("分析完毕！")
                
            except Exception as e:
                QMessageBox.critical(self, 'Prediction Error', str(e))
                self.statusBar.showMessage("Error during analysis")
            
            self.progress_bar.setMaximum(100)
            self.progress_bar.setValue(100)
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
            self.progress_bar.setMaximum(100)
            self.statusBar.showMessage("Error during analysis")

    def save_results(self):
        if not os.path.exists(os.path.join(self.output_dir, "result_image.png")):
            QMessageBox.warning(self, "Warning", "无检测结果，请先进行检测。")
            return
            
        save_path, _ = QFileDialog.getSaveFileName(
            self, 
            'Save Results', 
            os.path.join(QDir.homePath(), 'building_change_result.png'), 
            'PNG Image (*.png)'
        )
        
        if save_path:
            try:
                import shutil
                shutil.copy(
                    os.path.join(self.output_dir, "result_image.png"),
                    save_path
                )
                self.statusBar.showMessage(f"结果已保存至 {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save results: {str(e)}")
                self.statusBar.showMessage("保存出错")