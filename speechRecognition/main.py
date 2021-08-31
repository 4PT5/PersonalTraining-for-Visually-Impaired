import sys
import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, \
    QMessageBox, QPushButton, QMainWindow, QAction, qApp, QMenu, \
    QHBoxLayout, QFrame, QSplitter,  QVBoxLayout, QWidget, QTextEdit, QLabel
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QIcon, QPixmap
from stt import sttFunction


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.center()
        self.initUI()

    def initUI(self):
        # 메세지 박스를 통해 시작
        buttonReply = QMessageBox.question(
            self, 'Start message', "Personal Training을 시작하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if self.startMessage:
            self.setWindowTitle('PersonalTraining for Visually Impaired')
            self.disply_width = 1376
            self.display_height = 774
            self.webcam_width = 1280
            self.webcam_height = 720
            self.resize(1376, 774)  # 16:9
            self.center()
            self.setWindowIcon(QIcon('./image/Icon.png'))  # 아이콘 추가
            self.qSplitter()

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

        dropdownMenu = QPushButton('Select Exercise')
        menu = QMenu(self)
        menu.addAction('Squat')
        menu.addAction('exercise 1')
        menu.addAction('exercise 2')
        dropdownMenu.setMenu(menu)

        btn1 = QPushButton()
        btn1.setStyleSheet('image:url(./image/exit-icon.png)')
        btn1.clicked.connect(QCoreApplication.instance().quit)

        top_layout1.addSpacing(900)
        top_layout1.addWidget(dropdownMenu)
        top_layout1.addWidget(btn1)

        top = QFrame()
        top.setFrameShape(QFrame.NoFrame)
        top.setFrameShadow(QFrame.Plain)
        top.setLayout(top_layout1)

        bottom_layout = QHBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.resize(self.webcam_width, self.webcam_height)

        # create a vertical box layout and add the two labels
        bottom_layout.addWidget(self.image_label)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

        bottom = QFrame()
        bottom.setFrameShape(QFrame.NoFrame)
        bottom.setFrameShadow(QFrame.Plain)
        bottom.setLayout(bottom_layout)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(top)
        splitter1.addWidget(bottom)
        splitter1.setSizes([1, 400])

        vbox.addWidget(splitter1)
        self.setLayout(vbox)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            self.webcam_width, self.webcam_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = MyApp()
    a.show()
    sys.exit(app.exec_())
