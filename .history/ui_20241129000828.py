from mplwidget import MplWidget
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Thiết lập cửa sổ chính
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)  # Đặt kích thước cho cửa sổ chính

        # Tạo widget trung tâm cho giao diện
        self.central_widget = QtWidgets.QWidget(parent=MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.setStyleSheet("background-color: #d3d3d3;")  # Đặt màu nền xám mờ bóng

        # Tiêu đề chính
        self.title_label = QtWidgets.QLabel(parent=self.central_widget)
        self.title_label.setGeometry(QtCore.QRect(10, 10, 1180, 50))  # Đặt vị trí và kích thước
        self.title_label.setText("Thuật toán Hill Climbing cho bài toán Người du lịch")  # Nội dung tiêu đề
        self.title_label.setStyleSheet(
            "font-size: 40px; font-weight: bold; color: #333333;")  # Đặt kiểu chữ và màu sắc
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Canh giữa tiêu đề

        # Vùng hiển thị đồ thị
        self.canvasFrame = MplWidget(parent=self.central_widget)
        self.canvasFrame.setGeometry(QtCore.QRect(20, 70, 900, 500))  # Đặt vị trí và kích thước cho vùng đồ thị
        self.canvasFrame.setObjectName("canvasFrame")

        # SpinBox để nhập số lượng thành phố
        self.spinBox = QtWidgets.QSpinBox(parent=self.central_widget)
        self.spinBox.setGeometry(QtCore.QRect(940, 100, 200, 30))  # Đặt vị trí và kích thước
        self.spinBox.setMinimum(2)  # Giá trị nhỏ nhất là 2
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setStyleSheet(
            "font-size: 14px; padding: 5px; background-color: white; border-radius: 5px;")  # Kiểu dáng và màu nền

        # Nút "Bắt đầu"
        self.startButton = QtWidgets.QPushButton(parent=self.central_widget)
        self.startButton.setGeometry(QtCore.QRect(940, 150, 100, 40))  # Đặt vị trí và kích thước
        self.startButton.setObjectName("startButton")
        self.startButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(0, 170, 255);
                color: white;
                border-radius: 8px;
                font-size: 16px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: rgb(0, 150, 255);
            }
        """)  # Kiểu dáng khi di chuột và khi nhấn

        # Nút "Dừng lại"
        self.stopButton = QtWidgets.QPushButton(parent=self.central_widget)
        self.stopButton.setGeometry(QtCore.QRect(1050, 150, 100, 40))  # Đặt vị trí cùng hàng với nút "Bắt đầu"
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 77, 77);
                color: white;
                border-radius: 8px;
                font-size: 16px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: rgb(255, 50, 50);
            }
        """)  # Kiểu dáng khi di chuột và khi nhấn

        # Hộp văn bản hiển thị kết quả
        self.resultTextBox = QtWidgets.QTextBrowser(parent=self.central_widget)
        self.resultTextBox.setGeometry(QtCore.QRect(20, 580, 1160, 150))  # Đặt vị trí và kích thước
        self.resultTextBox.setObjectName("resultTextBox")
        self.resultTextBox.setStyleSheet(
            "background-color: white; border-radius: 5px; font-size: 14px;")  # Đặt màu nền và kiểu dáng

        # Đặt widget trung tâm
        MainWindow.setCentralWidget(self.central_widget)

        # MenuBar và StatusBar
        self.menu_bar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1200, 22))  # Đặt vị trí và kích thước
        self.menu_bar.setObjectName("menu_bar")
        MainWindow.setMenuBar(self.menu_bar)

        self.status_bar = QtWidgets.QStatusBar(parent=MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        # Gọi hàm đặt văn bản cho các thành phần
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hill Climbing for Travel Salesman Problem"))  # Tiêu đề cửa sổ
        self.startButton.setText(_translate("MainWindow", "Bắt đầu"))  # Văn bản trên nút "Bắt đầu"
        self.stopButton.setText(_translate("MainWindow", "Dừng lại"))  # Văn bản trên nút "Dừng lại"
