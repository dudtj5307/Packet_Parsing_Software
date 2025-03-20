from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QLabel, QHBoxLayout, QWidget
from PyQt6.QtGui import QMovie

class CustomListWidgetItem(QWidget):
    def __init__(self, text, gif_path, parent=None):
        super().__init__(parent)

        # 수평 레이아웃 생성
        layout = QHBoxLayout(self)

        # 텍스트 설정
        self.label = QLabel(text)
        layout.addWidget(self.label)

        # 로딩 GIF 설정
        self.loading_label = QLabel()
        self.movie = QMovie("GUI/res/loading_spinner.gif")
        self.loading_label.setMovie(self.movie)
        self.movie.start()  # 애니메이션 시작
        layout.addWidget(self.loading_label)

        # 레이아웃 설정
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)