import sys
from typing import Optional
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QVBoxLayout, QLabel
import PyQt6.QtWidgets as QtWidgets
from matplotlib.backend_bases import FigureCanvasBase
from ui import Ui_MainWindow  # Import giao diện được tạo từ Qt Designer
from algorithm import *  # Import các thuật toán được sử dụng
import asyncio
from qasync import QEventLoop, asyncSlot  # Hỗ trợ asyncio trong PyQt
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool, QCoreApplication
import qtinter  # Thư viện hỗ trợ tích hợp asyncio với PyQt
import random
import numpy as np
import pyqtgraph as pg
from decimal import Decimal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# Class hiển thị hộp thoại cảnh báo
class WarningDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")  # Tiêu đề của hộp thoại
        self.set
        self.setFixedWidth(300)  # Chiều rộng cố định
        self.setFixedHeight(100)  # Chiều cao cố định
        self.setModal(True)  # Đặt modal để ngăn các tác vụ khác cho đến khi hộp thoại được đóng
        self.layout = QVBoxLayout()  # Layout theo chiều dọc
        if message is None:
            self.message_label = QLabel("Please enter the number of destinations")  # Nội dung mặc định
        else:
            self.message_label = QLabel(message)  # Nội dung từ tham số
        self.layout.addWidget(self.message_label)  # Thêm nội dung vào layout
        self.setLayout(self.layout)  # Thiết lập layout cho hộp thoại

# Class ứng dụng chính
class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.is_running = False  # Cờ để kiểm tra xem quá trình đang chạy hay không
        self.ui = Ui_MainWindow()  # Tạo giao diện chính
        self.ui.setupUi(self)  # Thiết lập giao diện
        self.ui.startButton.clicked.connect(self.start_process)  # Kết nối nút "Start" với hàm start_process
        self.ui.stopButton.clicked.connect(self.stop_process)  # Kết nối nút "Stop" với hàm stop_process
        self.task = None  # Nhiệm vụ hiện tại
        self.graph = None  # Đồ thị hiện tại

    # Hàm bắt đầu quá trình
    def start_process(self):
        if not self.is_running:  # Nếu chưa chạy
            self.is_running = True  # Đánh dấu là đang chạy
            self.ui.canvasFrame.setVisible(True)  # Hiển thị khung vẽ đồ thị
            print("Start")  # In ra thông báo bắt đầu
            try:
                distance_matrix = create_distance_matrix(int(self.ui.spinBox.value()))  # Tạo ma trận khoảng cách
                hill_climbing = HillClimbing(int(self.ui.spinBox.value()))  # Tạo đối tượng Hill Climbing
                result = hill_climbing.solve()  # Giải bài toán

                # Hiển thị kết quả trong cửa sổ giao diện
                self.ui.resultTextBox.setText(hill_climbing.result)

                # Xóa đồ thị cũ trong khung vẽ
                self.ui.canvasFrame.canvas.axes.clear()
                distance_array = np.array(hill_climbing.matrix)  # Ma trận khoảng cách dưới dạng numpy array
                graph = nx.from_numpy_array(distance_array)  # Tạo đồ thị từ ma trận
                positions = nx.spring_layout(graph)  # Tính toán vị trí các nút trên đồ thị

                # Vẽ các thành phố (nút) trên đồ thị
                nx.draw_networkx_nodes(graph, positions, node_color='red', node_size=700, ax=self.ui.canvasFrame.canvas.axes)
                nx.draw_networkx_labels(graph, positions, font_size=10, font_color='white', ax=self.ui.canvasFrame.canvas.axes)

                # Xóa các cạnh cũ khỏi đồ thị
                graph.remove_edges_from(list(graph.edges()))

                # Tô màu các cạnh dựa trên trọng số
                threshold = 100  # Ngưỡng để phân biệt màu
                for (u, v, d) in graph.edges(data=True):
                    nx.draw_networkx_edges(
                        graph,
                        positions,
                        edgelist=[(u, v)],
                        edge_color='blue' if d.get('weight', 0) > threshold else 'green',
                        width=2,
                        ax=self.ui.canvasFrame.canvas.axes
                    )

                # Tô màu đường tốt nhất (màu xanh dương đậm)
                for i in range(len(result) - 1):
                    graph.add_edge(result[i], result[i + 1])
                nx.draw_networkx_edges(graph, positions, edgelist=list(graph.edges()), edge_color='blue', width=2, ax=self.ui.canvasFrame.canvas.axes)

                # Tô màu đường khép kín (màu xanh lá cây, nét đứt)
                graph.add_edge(result[-1], result[0])
                nx.draw_networkx_edges(graph, positions, edgelist=[(result[-1], result[0])], edge_color='green', width=2, style='dashed', ax=self.ui.canvasFrame.canvas.axes)

                self.graph = graph  # Lưu đồ thị hiện tại
                self.ui.canvasFrame.canvas.draw()  # Vẽ đồ thị lên giao diện
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")  # Hiển thị lỗi nếu có
                self.is_running = False  # Đặt lại trạng thái cờ
        else:
            dialog = WarningDialog("Please stop the current process")  # Hiển thị cảnh báo nếu quá trình đang chạy
            dialog.exec()

    # Hàm dừng quá trình
    def stop_process(self):
        if self.is_running:  # Nếu đang chạy
            self.is_running = False  # Đặt lại trạng thái cờ
            print("Stop")  # In ra thông báo dừng
            self.ui.resultTextBox.setText("")  # Xóa kết quả trên giao diện
            self.ui.canvasFrame.setVisible(False)  # Ẩn khung vẽ đồ thị
            QMessageBox.information(self, "Notice", "The process has been stopped.")  # Hiển thị thông báo đã dừng

# Hàm chính của chương trình
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Tạo ứng dụng PyQt
    window = MainApp()  # Tạo cửa sổ chính
    plt.axis('off')  # Tắt hiển thị trục trên đồ thị
    plt.xlim(0, 100)  # Đặt giới hạn trục x
    plt.ylim(0, 100)  # Đặt giới hạn trục y
    with qtinter.using_qt_from_asyncio():  # Sử dụng asyncio với PyQt
        window.show()  # Hiển thị cửa sổ chính
        sys.exit(app.exec())  # Chạy ứng dụng và thoát khi kết thúc
