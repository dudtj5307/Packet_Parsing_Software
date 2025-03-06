import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic

form_class = uic.loadUiType("main.ui")[0]

class MainWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_start.clicked.connect(self.start_sniffing)
        self.btn_stop.clicked.connect(self.stop_sniffing)
        self.btn_raw_open.clicked.connect(self.open_raw_file)
        self.btn_csv_open.clicked.connect(self.open_csv_file)
        self.btn_csv_create.clicked.connect(self.csv_create_file)
        self.btn_csv_view.clicked.connect(self.csv_open_folder)
        self.btn_csv_folder.clicked.connect(self.csv_open_folder)

    def open_settings(self):
        print("open_settings")

    def start_sniffing(self):
        print("start_sniffing")

    def stop_sniffing(self):
        print("stop_sniffing")

    def open_raw_file(self):
        print("open_raw_file")

    def open_csv_file(self):
        print("open_csv_file")





if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = MainWindow()
    myWindow.show()

    app.exec()