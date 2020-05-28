import sys
import os

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from physicoModule import config, PhysicoManage
from physico_main import PhysicoMain

current_dir = os.getcwd()
physicoUI = os.path.join(current_dir, 'uiFiles', 'physico_intro.ui')


class PhysicoIntro(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(physicoUI, self)
        self.initUI()
        self.initial_directory = None

    def initUI(self):
        qPixmapVar = QPixmap()
        pix_path = os.path.join(current_dir, 'iconFiles', 'parkcoach.png')
        qPixmapVar.load(pix_path)
        qPixmapVar = qPixmapVar.scaledToWidth(250)
        self.labelIntro.setPixmap(qPixmapVar)

        self.pushButtonNew.clicked.connect(self.new)

        self.pushButtonStart.clicked.connect(self.start)

        self.pushButtonQuit.clicked.connect(QCoreApplication.instance().quit)

        self.show()

    # @pyqtSlot
    def new(self):
        select_directory = QFileDialog.getExistingDirectory(
            self, "Select Folder", self.initial_directory)
        f = open(os.path.join(select_directory, 'physico_project.psj'), 'w')
        f.close()
        select_files = QFileDialog.getOpenFileNames(
            self, "Select File", self.initial_directory, 'excel file (*.xlsx)')
        print(select_files[0])
        # pManage = PhysicoManage(select_directory)
        # pManage.updateManager()
        # self.ex1 = PhysicoMain(select_directory)

    def start(self):
        select_directory = QFileDialog.getExistingDirectory(
            self, "Select Folder", self.initial_directory)
        print(select_directory)
        if os.path.isfile(os.path.join(select_directory, 'physico_project.psj')):
            pManage = PhysicoManage(select_directory)
            pManage.updateManager()
            self.ex1 = PhysicoMain(select_directory)
        else:
            self.showPopupMsg(
                'Directory Error.', '{} is not physico project directory.\nPlz check again!!'.format(select_directory))

    def showPopupMsg(self, title, content):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(content)
        msg.setStandardButtons(QMessageBox.Ok)
        result = msg.exec_()
        if result == QMessageBox.Ok:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhysicoIntro()
    # ex.show()
    sys.exit(app.exec_())
