from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from PyQt5.QtWebEngineWidgets import *
import PyQt5
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import plotly.offline as po
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from physicoModule import config, PhysicoManage, PhysicoControl, PhysicoMatch, ExcelWrite, ExcelMatch, ExcelChart, ExcelStyle, PhysicoPlayerGraph, PhysicoDayGraph, PhysicoMatchGraph, PhysicoPlotly
from pandas_model import DataFrameModel, PandasModel

current_dir = os.getcwd()
physicoUI = os.path.join(current_dir, 'uiFiles', 'physico_main.ui')


class PhysicoMain(QWidget):

    def __init__(self, base_dir):
        super().__init__()
        uic.loadUi(physicoUI, self)
        self.initUI(base_dir)

    def initUI(self, base_dir):
        self.pManage = PhysicoManage(base_dir)
        self.runTab()
        date_list = list(self.pManage.file_set.keys())
        if date_list:
            period = len(date_list)
            start_day = date_list[0]
            end_day = date_list[-1]
            self.labelIntro.setText(
                "We worked out for {} days. From {} to {}".format(period, start_day, end_day))
        else:
            pass
        # Intro
        # self.pushButtonQuit.clicked.connect(QCoreApplication.instance().quit)
        self.pushButtonQuit.clicked.connect(self.mainClose)
        self.pushButtonIntroRun.clicked.connect(self.introRun)
        # Day
        self.pushButtonDayRun.clicked.connect(self.dayRun)
        self.comboDayDate.currentIndexChanged.connect(self.dayRun)
        self.pushButtonDaySave.clicked.connect(self.daySave)
        # D-Graph
        self.pushButtonDGraphRun.clicked.connect(self.dayGraphRun)
        self.comboGraphDate.currentIndexChanged.connect(self.dayGraphRun)
        self.checkDayValue.stateChanged.connect(self.dayGraphRun)
        self.pushButtonDGraphSave.clicked.connect(self.dayGraphSave)
        # Match
        self.pushButtonMatchRun.clicked.connect(self.matchRun)
        self.comboMatchDate.currentIndexChanged.connect(self.matchRun)
        self.pushButtonMatchSave.clicked.connect(self.matchSave)
        # M-Graph
        self.pushButtonMGraphRun.clicked.connect(self.matchGraphRun)
        self.comboMGraphDate.currentIndexChanged.connect(self.matchGraphRun)
        self.checkMatchValue.stateChanged.connect(self.matchGraphRun)
        self.pushButtonMGraphSave.clicked.connect(self.matchGraphSave)
        # Player
        self.pushButtonPlayerRun.clicked.connect(self.playerRun)
        self.comboPlayerName.currentIndexChanged.connect(self.playerRun)
        self.pushButtonPlayerSave.clicked.connect(self.playerSave)
        # P-Graph
        self.pushButtonPGraphRun.clicked.connect(self.playerGraphRun)
        self.comboGraphPlayer.currentIndexChanged.connect(self.playerGraphRun)
        self.checkPlayerValue.stateChanged.connect(self.playerGraphRun)
        self.pushButtonPGraphSave.clicked.connect(self.playerGraphSave)
        # Save
        self.pushButtonAllDaySave.clicked.connect(self.allDaySave)
        self.pushButtonAllPlayerSave.clicked.connect(self.allPlayerSave)
        self.pushButtonPtypeGraphSave.clicked.connect(self.playerTypeGraphSave)
        self.pushButtonDtypeGraphSave.clicked.connect(self.dayTypeGraphSave)

        # for plotly graph
        # self.pushButtonTEST.clicked.connect(self.plotlyTest)

        self.show()

    # def plotlyTest(self):
    #     Phyly = PhysicoPlotly(self.pManage)
    #     fig = Phyly.makeSinglePlotly('JI Soyun')

    #     raw_html = '<html><head><meta charset="utf-8" />'
    #     raw_html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
    #     raw_html += '<body>'
    #     raw_html += po.plot(fig, include_plotlyjs=False, output_type='div')
    #     raw_html += '</body></html>'

    #     # setHtml has a 2MB size limit, need to switch to setUrl on tmp file
    #     # for large figures.
    #     self.webEngineView.setHtml(raw_html)
    #     self.webEngineView.show()
    #     # self.webEngineView.raise_()

    def mainClose(self):
        self.close()

    def runTab(self):
        d_set = self.pManage.day_set
        p_set = self.pManage.player_set
        m_set = self.pManage.match_set
        # Day / D-Graph tab
        self.comboDayDate.clear()
        self.comboGraphDate.clear()
        for day in d_set.keys():
            self.comboDayDate.addItem(day)
            self.comboGraphDate.addItem(day)
        # Match / M-Graph tab
        self.comboMatchDate.clear()
        self.comboMGraphDate.clear()
        for match in m_set.keys():
            matchCamp = match[0]
            matchDate = match[1]
            matchName = match[2]
            matchInfo = matchCamp + ":" + matchDate + ":" + matchName
            self.comboMatchDate.addItem(matchInfo)
            self.comboMGraphDate.addItem(matchInfo)
        # Player / P-Graph tab
        self.comboPlayerName.clear()
        for player in p_set.keys():
            self.comboPlayerName.addItem(player)
        # Graph tab
        self.comboGraphPlayer.clear()
        self.comboGraphFrom.clear()
        self.comboGraphTo.clear()
        for player in p_set.keys():
            self.comboGraphPlayer.addItem(player)
        for day in d_set.keys():
            self.comboGraphFrom.addItem(day)
            self.comboGraphTo.addItem(day)
        # Save tab
        self.comboSaveFrom.clear()
        self.comboSaveTo.clear()
        self.comboSavePtypeGraph.clear()
        self.comboSaveDtypeGraph.clear()
        # self.comboSaveDate.clear()
        for day in d_set.keys():
            self.comboSaveFrom.addItem(day)
            self.comboSaveTo.addItem(day)
            # self.comboSaveDate.addItem(day[0])
        for item in ['Distance', 'Load', 'Mono, Strain', 'MSR', 'HSR', 'Sprint']:
            self.comboSavePtypeGraph.addItem(item)
        for item in ['Position Distance', 'Player Distance', 'Mono, Strain', 'Weight Change']:
            self.comboSaveDtypeGraph.addItem(item)

    # Intro
    def introRun(self):
        self.pManage.updateManager()
        date_list = list(self.pManage.file_set.keys())
        if date_list:
            period = len(date_list)
            start_day = date_list[0]
            end_day = date_list[-1]
            self.labelIntro.setText(
                "We worked out for {} days. From {} to {}".format(period, start_day, end_day))
        else:
            pass
        self.runTab()
        self.showPopupComplete('Complete', 'input file 처리를 완료했습니다.')

    # Day

    def dayRun(self):
        current_date = self.comboDayDate.currentText()
        Controler = PhysicoControl(self.pManage)
        day_excel = Controler.makeDayExcelData(int(current_date[:8]))
        day_model = PandasModel(day_excel['day'])
        position_model = PandasModel(day_excel['position'])
        self.tableViewDay.setModel(day_model)
        self.tableViewPosition.setModel(position_model)

    def daySave(self):
        current_date = self.comboDayDate.currentText()
        ExcelWriter = ExcelWrite(self.pManage)
        ExcelWriter.writeDayExcel(int(current_date[:8]))
        self.showPopupComplete(
            'Complete', "Day({}) Excel Save complete!!".format(current_date))

    # D-Graph
    def dayGraphRun(self):
        current_date = self.comboGraphDate.currentText()

        graph_type = []
        if self.checkDDistancePosition.isChecked() == True:
            graph_type.append('Position Distance')
        if self.checkDDistancePlayer.isChecked() == True:
            graph_type.append('Player Distance')
        if self.checkDMono.isChecked() == True:
            graph_type.append('Day Mono, Strain')
        if self.checkDAccel.isChecked() == True:
            graph_type.append('Player Accel, Decel')
        if self.checkDWeight.isChecked() == True:
            graph_type.append('Day Weight Change')
        if self.checkDBI.isChecked() == True:
            graph_type.append('Day Body Index')

        if self.checkDayValue.isChecked():
            value_on = True
        else:
            value_on = False

        Grapher = PhysicoDayGraph(self.pManage)
        fig = Grapher.makeGraph(current_date, graph_type, False, value_on)

        if not fig is None:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Fixed)
            # canvas.setFocusPolicy(Qt.ClickFocus)
            # canvas.setFocus()
            canvas.draw()
            self.scrollAreaDayGraph.setWidget(canvas)
            canvas.show()

    def dayGraphSave(self):
        current_date = self.comboGraphDate.currentText()

        graph_type = []
        if self.checkDDistancePosition.isChecked() == True:
            graph_type.append('Position Distance')
        if self.checkDDistancePlayer.isChecked() == True:
            graph_type.append('Player Distance')
        if self.checkDMono.isChecked() == True:
            graph_type.append('Day Mono, Strain')
        if self.checkDAccel.isChecked() == True:
            graph_type.append('Player Accel, Decel')
        if self.checkDWeight.isChecked() == True:
            graph_type.append('Day Weight Change')
        if self.checkDBI.isChecked() == True:
            graph_type.append('Day Body Index')

        if self.checkDayValue.isChecked():
            value_on = True
        else:
            value_on = False

        Grapher = PhysicoDayGraph(self.pManage)
        Grapher.makeGraph(current_date, graph_type, True, value_on)
        self.showPopupComplete(
            'Complete', "{} Graph Save complete!!".format(current_date))

    # Match
    def matchRun(self):
        current_match = self.comboMatchDate.currentText()
        current_camp, current_date, current_info = current_match.split(':')
        Matcher = PhysicoMatch(self.pManage)
        day_excel = Matcher.matchTeamData(
            current_camp, current_date, current_info)
        day_model = PandasModel(day_excel['day'])
        position_model = PandasModel(day_excel['position'])
        self.tableViewMatch.setModel(day_model)
        self.tableViewMatchPosition.setModel(position_model)

    def matchSave(self):
        current_match = self.comboMatchDate.currentText()
        current_camp, current_date, current_info = current_match.split(':')
        ExcelWriter = ExcelMatch(self.pManage)
        ExcelWriter.writeMatchExcel(current_camp, current_date, current_info)
        self.showPopupComplete(
            'Complete', "Match({}) Excel Save complete!!".format(current_date))
        pass

    # M-Graph
    def matchGraphRun(self):
        current_date = self.comboMGraphDate.currentText()
        [matchCamp, matchDate, matchName] = current_date.split(':')

        graph_type = []
        if self.checkMDistancePosition.isChecked() == True:
            graph_type.append('Position Distance')
        if self.checkMDistancePlayer.isChecked() == True:
            graph_type.append('Player Distance')
        if self.checkMTimeDistance.isChecked() == True:
            graph_type.append('Player Total Time & Dist.')
        if self.checkMTimeHSR.isChecked() == True:
            graph_type.append('Player Total Time & HSR')
        if self.checkMTimeSprint.isChecked() == True:
            graph_type.append('Player Total Time & Sprint')
        if self.checkMAccel.isChecked() == True:
            graph_type.append('Player Accel, Decel')

        if self.checkMatchValue.isChecked():
            value_on = True
        else:
            value_on = False

        Grapher = PhysicoMatchGraph(self.pManage)
        fig = Grapher.makeGraph(matchCamp, matchDate,
                                matchName, graph_type, False, value_on)

        if not fig is None:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Fixed)
            # canvas.setFocusPolicy(Qt.ClickFocus)
            # canvas.setFocus()
            canvas.draw()
            self.scrollAreaMatchGraph.setWidget(canvas)
            canvas.show()

    def matchGraphSave(self):
        current_date = self.comboMGraphDate.currentText()
        [matchCamp, matchDate, matchName] = current_date.split(':')

        graph_type = []
        if self.checkMDistancePosition.isChecked() == True:
            graph_type.append('Position Distance')
        if self.checkMDistancePlayer.isChecked() == True:
            graph_type.append('Player Distance')
        if self.checkMTimeDistance.isChecked() == True:
            graph_type.append('Player Total Time & Dist.')
        if self.checkMTimeHSR.isChecked() == True:
            graph_type.append('Player Total Time & HSR')
        if self.checkMTimeSprint.isChecked() == True:
            graph_type.append('Player Total Time & Sprint')
        if self.checkMAccel.isChecked() == True:
            graph_type.append('Accel, Decel')

        if self.checkMatchValue.isChecked():
            value_on = True
        else:
            value_on = False

        Grapher = PhysicoMatchGraph(self.pManage)
        Grapher.makeGraph(matchCamp, matchDate, matchName,
                          graph_type, True, value_on)
        self.showPopupComplete(
            'Complete', "{} Graph Save complete!!".format(current_date))

    # Player

    def playerRun(self):
        current_player = self.comboPlayerName.currentText()
        Controler = PhysicoControl(self.pManage)
        player_excel = Controler.makePlayerExcelData()
        player_df = player_excel[current_player]
        model = PandasModel(player_df)
        self.tableViewPlayer.setModel(model)

    def playerSave(self):
        current_player = self.comboPlayerName.currentText()
        ExcelWriter = ExcelWrite(self.pManage)
        ExcelWriter.writePlayerExcel(current_player)
        self.showPopupComplete(
            'Complete', "{}'s Excel Save complete!!".format(current_player))

    # P-Graph

    def playerGraphRun(self):
        current_player = self.comboGraphPlayer.currentText()
        current_from = self.comboGraphFrom.currentText()
        current_to = self.comboGraphTo.currentText()
        # current_from = int(current_from)
        # current_to = int(current_to)

        graph_type = []
        if self.checkDistance.isChecked() == True:
            graph_type.append(self.checkDistance.text())
        if self.checkLoad.isChecked() == True:
            graph_type.append(self.checkLoad.text())
        if self.checkMono.isChecked() == True:
            graph_type.append(self.checkMono.text())
        if self.checkMSR.isChecked() == True:
            graph_type.append(self.checkMSR.text())
        if self.checkHSR.isChecked() == True:
            graph_type.append(self.checkHSR.text())
        if self.checkSprint.isChecked() == True:
            graph_type.append(self.checkSprint.text())
        if self.checkSleep.isChecked() == True:
            graph_type.append(self.checkSleep.text())
        if self.checkWeight.isChecked() == True:
            graph_type.append('Weight Change')
        if self.checkBI.isChecked() == True:
            graph_type.append(self.checkBI.text())

        if self.checkPlayerValue.isChecked():
            value_on = True
        else:
            value_on = False

        Grapher = PhysicoPlayerGraph(self.pManage)
        fig = Grapher.makeGraph(
            current_player, current_from, current_to, graph_type, False, value_on)

        if not fig is None:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Fixed)
            # canvas.setFocusPolicy(Qt.ClickFocus)
            # canvas.setFocus()
            canvas.draw()
            self.scrollAreaPlayerGraph.setWidget(canvas)
            canvas.show()
        else:
            print('Nothing! ')

    def playerGraphSave(self):
        current_player = self.comboGraphPlayer.currentText()
        current_from = self.comboGraphFrom.currentText()
        current_to = self.comboGraphTo.currentText()

        graph_type = []
        if self.checkDistance.isChecked() == True:
            graph_type.append(self.checkDistance.text())
        if self.checkLoad.isChecked() == True:
            graph_type.append(self.checkLoad.text())
        if self.checkMono.isChecked() == True:
            graph_type.append(self.checkMono.text())
        if self.checkMSR.isChecked() == True:
            graph_type.append(self.checkMSR.text())
        if self.checkHSR.isChecked() == True:
            graph_type.append(self.checkHSR.text())
        if self.checkSprint.isChecked() == True:
            graph_type.append(self.checkSprint.text())
        if self.checkSleep.isChecked() == True:
            graph_type.append(self.checkSleep.text())
        if self.checkWeight.isChecked() == True:
            graph_type.append('Weight Change')
        if self.checkBI.isChecked() == True:
            graph_type.append(self.checkBI.text())
        if self.checkPlayerValue.isChecked():
            value_on = True
        else:
            value_on = False

        Grapher = PhysicoPlayerGraph(self.pManage)
        Grapher.makeGraph(
            current_player, current_from, current_to, graph_type, True, value_on)
        self.showPopupComplete(
            'Complete', "{}'s Graph Save complete!!".format(current_player))

    # Save

    def allDaySave(self):
        ExcelWriter = ExcelWrite(self.pManage)
        ExcelWriter.writeDayExcel()
        self.showPopupComplete('Complete', "Day Excel Save complete!!")

    def allPlayerSave(self):
        ExcelWriter = ExcelWrite(self.pManage)
        ExcelWriter.writePlayerExcel()
        self.showPopupComplete('Complete', "Player's Excel Save complete!!")

    def playerTypeGraphSave(self):
        current_from = self.comboSaveFrom.currentText()
        current_to = self.comboSaveTo.currentText()
        current_type = self.comboSavePtypeGraph.currentText()
        if self.checkVPG.isChecked():
            value_on = True
        else:
            value_on = False
        for name in self.pManage.player_set.keys():
            Grapher = PhysicoPlayerGraph(self.pManage)
            Grapher.makeSingleGraph(name, current_from,
                                    current_to, [current_type], True, value_on)
        self.showPopupComplete('Complete', 'Graph Save complete!!')

    # TODO
    def dayTypeGraphSave(self):
        current_type = self.comboSaveDtypeGraph.currentText()
        if self.checkVDG.isChecked():
            value_on = True
        else:
            value_on = False
        for day in self.pManage.day_set.keys():
            Grapher = PhysicoDayGraph(self.pManage)
            Grapher.makeSingleGraph(day, [current_type], True, value_on)
        self.showPopupComplete('Complete', 'Graph Save complete!!')

    def setLabelSave(self, content):
        self.labelSave.setText(content)

    def showPopupComplete(self, title, content):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(content)
        msg.setStandardButtons(QMessageBox.Ok)
        result = msg.exec_()
        if result == QMessageBox.Ok:
            self.labelSave.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhysicoMain()
    ex.show()
    sys.exit(app.exec_())
