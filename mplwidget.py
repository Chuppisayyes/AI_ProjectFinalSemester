from PyQt6.QtWidgets import *  # Import các widget từ PyQt6

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas  # Import canvas cho Matplotlib
from matplotlib.pyplot import figure  # Import đối tượng figure từ Matplotlib
from matplotlib.figure import Figure  # Import lớp Figure từ Matplotlib

# Lớp MplWidget dùng để tạo khung hiển thị đồ thị Matplotlib
class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)  # Gọi hàm khởi tạo của lớp QWidget
        self.figure = figure(figsize=(100, 100))  # Tạo đối tượng figure với kích thước lớn
        self.figure.gca().axis('off')  # Ẩn các trục trên đồ thị
        self.canvas = FigureCanvas(self.figure)  # Tạo canvas từ figure
        vertical_layout = QVBoxLayout()  # Tạo layout theo chiều dọc
        vertical_layout.addWidget(self.canvas)  # Thêm canvas vào layout
        self.canvas.axes = self.figure.add_subplot(111)  # Thêm một subplot (trục tọa độ) vào figure
        self.setLayout(vertical_layout)  # Đặt layout cho widget
