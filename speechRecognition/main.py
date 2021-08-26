import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox, QPushButton
from PyQt5.QtCore import QCoreApplication


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
