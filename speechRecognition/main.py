import sys
from PyQt5 import QtCore
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, \
    QMessageBox, QPushButton, QMainWindow, QAction, qApp, QMenu, \
    QHBoxLayout, QFrame, QSplitter,  QVBoxLayout, QWidget, QTextEdit, QLabel
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from stt import sttFunction


class MyApp(QWidget): 

    def __init__(self):
        super().__init__()
        self.center()
        self.initUI()

    def initUI(self):
        # quit 버튼
        # self.quitButton()
        # 메세지 박스를 통해 시작
        buttonReply = QMessageBox.question(
            self, 'Start message', "Personal Training을 시작하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if self.startMessage:
            self.setWindowTitle('PersonalTraining for Visually Impaired')
            self.resize(1376, 774)  # 16:9
            self.center()
            self.setWindowIcon(QIcon('./image/Icon.png'))  # 아이콘 추가
            self.qSplitter()
            self.show()
        else:
            sys.exit()

    def center(self):  # 창을 화면 중앙으로
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startMessage(self):
        buttonReply = QMessageBox.question(
            self, 'Start message', "Personal Training을 시작하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            return True
        else:
            return False

    def quitButton(self):
        btn = QPushButton('Quit', self)
        btn.move(588, 710)
        btn.resize(200, 50)
        btn.clicked.connect(QCoreApplication.instance().quit)

    def qSplitter(self):
        vbox = QVBoxLayout()

        top_layout1 = QHBoxLayout()

        label1 = QLabel()
        label1.setStyleSheet('image:url(./image/main_logo.png);')

        dropdownMenu = QPushButton('Select Exercise')
        menu = QMenu(self)
        menu.addAction('Squat')
        menu.addAction('exercise 1')
        menu.addAction('exercise 2')
        dropdownMenu.setMenu(menu)

        btn1 = QPushButton()
        btn1.setStyleSheet('image:url(./image/exit-icon.png)')
        btn1.clicked.connect(QCoreApplication.instance().quit)

        top_layout1.addWidget(label1)
        top_layout1.addSpacing(900)
        top_layout1.addWidget(dropdownMenu)
        top_layout1.addWidget(btn1)

        top = QFrame()
        top.setFrameShape(QFrame.NoFrame)
        top.setFrameShadow(QFrame.Plain)
        top.setLayout(top_layout1)

        bottom = QFrame()
        bottom.setFrameShape(QFrame.NoFrame)
        bottom.setFrameShadow(QFrame.Plain)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(top)
        splitter1.addWidget(bottom)
        splitter1.setSizes([1, 400])

        vbox.addWidget(splitter1)
        self.setLayout(vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
