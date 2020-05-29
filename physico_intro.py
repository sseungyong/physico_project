import sys
import os
import shutil

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
        check_file_path = os.path.join(select_directory, 'physico_project.psj')
        if os.path.isfile(check_file_path):
            self.showPopupMsg(
                'Directory Error.', '{} is already physico project directory.\nPlz check again!!'.format(select_directory))
        else:
            f = open(check_file_path, 'w')
            f.close()
            input_data_directory = os.path.join(
                select_directory, '#01_input_data')
            workout_directory = os.path.join(
                input_data_directory, '#001_workout')
            wellness_directory = os.path.join(
                input_data_directory, '#002_wellness')
            os.makedirs(input_data_directory)
            os.makedirs(workout_directory)
            os.makedirs(wellness_directory)
            select_workout_files = QFileDialog.getOpenFileNames(
                self, "Select Workout File", self.initial_directory, 'excel file (*.xlsx)')
            select_workout_files_name = select_workout_files[0]
            print(type(select_workout_files_name))
            if not select_workout_files_name:
                print("0 files selected.")
            else:
                print("{} files selected".format(
                    len(select_workout_files_name)))
                for file_name in select_workout_files_name:
                    workout_basename = os.path.basename(file_name)
                    shutil.copyfile(file_name, os.path.join(
                        workout_directory, workout_basename))

            select_wellness_files = QFileDialog.getOpenFileNames(
                self, "Select wellness File", self.initial_directory, 'excel file (*.xlsx)')
            select_wellness_files_name = select_wellness_files[0]
            print(type(select_wellness_files_name))
            if not select_wellness_files_name:
                print("0 files selected.")
            else:
                print("{} files selected".format(
                    len(select_wellness_files_name)))
                for file_name in select_wellness_files_name:
                    wellness_basename = os.path.basename(file_name)
                    shutil.copyfile(file_name, os.path.join(
                        wellness_directory, wellness_basename))

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
