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

        self.pushButtonStart.clicked.connect(self.start)

        self.pushButtonQuit.clicked.connect(QCoreApplication.instance().quit)

        self.show()

    # @pyqtSlot
    def start(self):
        # print('click Start button!!')
        # appp = QApplication(sys.argv)
        # ex = PhysicoTrain()
        # ex.show()
        # sys.exit(appp.exec_())
        select_directory = QFileDialog.getExistingDirectory(
            self, "Select Folder", self.initial_directory)
        pManage = PhysicoManage(select_directory)
        pManage.updateManager()
        self.ex1 = PhysicoMain(select_directory)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhysicoIntro()
    # ex.show()
    sys.exit(app.exec_())
