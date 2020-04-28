import numpy as np
import pandas as pd
import os
import openpyxl
import configparser
from physicoModule import config
import matplotlib.pyplot as plt
from physicoModule.physico_control import PhysicoControl, PhysicoMatch
from physicoModule.physico_plotfnc import BARCOLOR, LINECOLOR, GRAPHUNIT, HIGHESTY, PLAYERGRAPHTYPE, DAYGRAPHTYPE, MATCHGRAPHTYPE, TRPOSITIONLIST, MPOSITIONLIST
from physicoModule.physico_plotfnc import plotBar, plotLine

# base_path = config.ROOT_CONFIG['base']
graph_path = config.FOLDER_CONFIG['graph']

# Parameter
FIGSIZEX = 24
FIGSIZEY = 8


class PhysicoPlayerGraph(PhysicoControl):
    def __init__(self, PMANAGE):
        super().__init__(PMANAGE)
        self.plyaer_gdict, self.team_gdata = self.__receiveData()
        self.unit_data = self.__loadUnitData()

    def __receiveData(self):
        player_gdict = self.player_set
        team_gdata = self.player_set['Team']
        return player_gdict, team_gdata

    def __loadUnitData(self):
        unitdata_path = os.path.join(self.base_path, 'unit_config.conf')
        cp = configparser.ConfigParser()
        cp.read(unitdata_path)
        print(unitdata_path)
        if 'HIGHESTY' in cp.sections():
            print("success load unit data!")
            return cp
        else:
            print("fail load unit data...")
            return None

    def settingData(self, name, fromDate, toDate, gtype):
        player_data = self.plyaer_gdict[name]
        player_data = player_data.set_index('Date')
        player_data = player_data.loc[fromDate: toDate, 'Camp':]
        player_data.loc[:, 'TR Time':] = player_data.loc[:,
                                                         'TR Time':].fillna(0)
        team_data = self.team_gdata.set_index('Date')
        team_data = team_data.loc[fromDate:toDate, 'Camp':]
        team_data.loc[:, 'TR Time':] = team_data.loc[:,
                                                     'TR Time':].fillna(0)
        player_data = player_data.round(1)
        team_data = team_data.round(1)
        # xlabel = np.array([str(x) for x in player_data.index.values])
        graph_setting = [PLAYERGRAPHTYPE[gt] for gt in gtype]

        return player_data, team_data, graph_setting

    def getBarData(self, player_data, team_data, contentDict):
        bar_type = contentDict['wannaType']
        if bar_type[2] == 'PG_Body Index':
            player_data = player_data[['Weight', 'Body Muscle', 'Body Fat']]
            player_data = player_data.replace(0, np.nan)
            player_data = player_data.dropna()
        content_list = contentDict['needData']
        bar_dict = {}
        for (name, content) in content_list:
            if name == 'Team':
                bar_dict[content+':Team'] = team_data[content]
            else:
                bar_dict[content] = player_data[content]

        xlabel = np.array([str(x) for x in player_data.index.values])

        return bar_type, bar_dict, xlabel

    def getLineData(self, player_data, team_data, contentDict):
        line_type = contentDict['wannaType']
        if line_type[2] == 'PG_Body Index':
            player_data = player_data[['Weight', 'Body Muscle', 'Body Fat']]
            player_data = player_data.replace(0, np.nan)
            player_data = player_data.dropna()
        content_list = contentDict['needData']
        line_dict = {}
        for (name, content) in content_list:
            if name == 'Team':
                line_dict[content+':Team'] = team_data[content]
            else:
                line_dict[content] = player_data[content]

        return line_type, line_dict

    def makeSingleGraph(self, name, fromDate, toDate, gtype, wannasave, val):
        if int(fromDate) > int(toDate):
            return None
        try:
            fig_size_x = int(self.unit_data['GRAPH SIZE']['Xsize'])
            fig_size_y = int(self.unit_data['GRAPH SIZE']['Ysize'])
        except:
            fig_size_x = FIGSIZEX
            fig_size_y = FIGSIZEY

        player_data, team_data, graph_setting = self.settingData(
            name, fromDate, toDate, gtype)
        bar_type, bar_data, xlabel = self.getBarData(
            player_data, team_data, graph_setting[0]['Bar'])
        line_type, line_data = self.getLineData(
            player_data, team_data, graph_setting[0]['Line'])

        # window setting
        fig, ax = plt.subplots(1, 1, figsize=(fig_size_x, fig_size_y))
        # fig.set_size_inches(fig_size_x, 6, forward=True)
        ax_twinx = ax.twinx()

        day_type = None
        # draw left graph
        plotBar(ax, day_type, bar_type, bar_data,
                xlabel, wannasave, val, name, self.unit_data, line_data)
        # draw right graph
        plotLine(ax_twinx, day_type, line_type,
                 line_data, xlabel, wannasave, val, name, self.unit_data, bar_data)

        if wannasave:
            fig.tight_layout()
            title = "{}'s {} graph ({}~{})".format(
                name, gtype[0], fromDate, toDate)
            save_path = os.path.join(
                self.base_path, graph_path, config.IMAGE_CONFIG[gtype[0]], title+'.png')
            plt.savefig(save_path, dpi=300)
            plt.close()
            return None
        else:
            fig.set_size_inches(fig_size_y, 4)
            fig.tight_layout()
            return fig

    def makeMultiGraph(self, name, fromDate, toDate, gtype, wannasave, val):
        if int(fromDate) > int(toDate):
            return None
        try:
            fig_size_x = int(self.unit_data['GRAPH SIZE']['Xsize'])
            fig_size_y = int(self.unit_data['GRAPH SIZE']['Ysize'])
        except:
            fig_size_x = FIGSIZEX
            fig_size_y = FIGSIZEY

        # data setting
        player_data, team_data, graph_setting = self.settingData(
            name, fromDate, toDate, gtype)

        fig_length = len(graph_setting)
        fig, ax = plt.subplots(fig_length, 1, figsize=(
            fig_size_x, fig_size_y*fig_length))
        # fig.set_size_inches(fig_size_x, 6*fig_length, forward=True)

        for gi, gt in enumerate(gtype):
            bar_type, bar_data, xlabel = self.getBarData(
                player_data, team_data, graph_setting[gi]['Bar'])
            line_type, line_data = self.getLineData(
                player_data, team_data, graph_setting[gi]['Line'])

            # window setting
            ax_twinx = ax[gi].twinx()
            day_type = None
            plotBar(ax[gi], day_type, bar_type, bar_data,
                    xlabel, wannasave, val, name, self.unit_data, line_data)
            # draw right graph
            plotLine(ax_twinx, day_type, line_type, line_data,
                     xlabel, wannasave, val, name, self.unit_data, bar_data)

        # graph label setting
        # plt.subplots_adjust(wspace=10.)
        fig.tight_layout()

        if wannasave:
            fig.tight_layout()
            title = "{}'s {} graph ({}~{})".format(
                name, 'Total', fromDate, toDate)
            save_path = os.path.join(
                self.base_path, graph_path, config.IMAGE_CONFIG['Total'], title+'.png')
            plt.savefig(save_path, dpi=300)
            plt.close()
            return None
        else:
            fig.set_size_inches(fig_size_y, 4*fig_length)
            fig.tight_layout()
            return fig

    def makeGraph(self, name, fromDate, toDate, gtype, wannasave, val):
        gnum = len(gtype)
        if gnum == 0:
            fig = None
        elif gnum == 1:
            fig = self.makeSingleGraph(
                name, fromDate, toDate, gtype, wannasave, val)
        else:
            fig = self.makeMultiGraph(
                name, fromDate, toDate, gtype, wannasave, val)
        return fig


class PhysicoDayGraph(PhysicoControl):
    def __init__(self, PMANAGE):
        super().__init__(PMANAGE)
        self.unit_data = self.__loadUnitData()

    def __loadUnitData(self):
        unitdata_path = os.path.join(self.base_path, 'unit_config.conf')
        cp = configparser.ConfigParser()
        cp.read(unitdata_path)
        print(unitdata_path)
        if 'HIGHESTY' in cp.sections():
            print("success load unit data!")
            return cp
        else:
            print("fail load unit data...")
            return None

    def settingData(self, date, gtype):
        if date in self.day_set.keys():
            player_name = self.day_set[date]['Player']
            position_data = self.day_set[date]['Data']
            day_type = 'TR'
        else:
            position_data = None
            day_type = None

        exist_list = []
        for position in TRPOSITIONLIST:
            if position in position_data.index:
                exist_list.append(position)
        position_data = position_data.reindex(index=exist_list)
        position_data = position_data.round(1)

        player_data = pd.DataFrame()
        for value in self.player_set.values():
            player_df = value.query("Date=='{}'".format(date))
            player_data = player_data.append(player_df)
        player_data.loc[:, 'TR Time':] = player_data.loc[:,
                                                         'TR Time':].fillna(0)
        player_data = player_data.loc[player_name, :]
        player_data = player_data.round(1)

        # sort by position order & drop position = NaN
        player_df = pd.DataFrame()
        for position in TRPOSITIONLIST:
            try:
                player_df = player_df.append(
                    player_data[player_data['Position'] == position])
            except:
                pass

        graph_setting = [DAYGRAPHTYPE[gt] for gt in gtype]

        return day_type, position_data, player_df, graph_setting

    def getBarData(self, position_data, player_data, contentDict):
        bar_type = contentDict['wannaType']
        content_list = contentDict['needData']
        bar_dict = {}
        for (name, content) in content_list:
            if name == 'Position':
                bar_dict[content] = position_data[content]
            else:
                bar_dict[content] = player_data[content]

        return bar_type, bar_dict

    def getLineData(self, position_data, player_data, contentDict):
        line_type = contentDict['wannaType']
        content_list = contentDict['needData']
        line_dict = {}
        for (name, content) in content_list:
            if name == 'Position':
                line_dict[content] = position_data[content]
            else:
                line_dict[content] = player_data[content]

        return line_type, line_dict

    def makeSingleGraph(self, date, gtype, wannasave, val):
        try:
            fig_size_x = int(self.unit_data['GRAPH SIZE']['Xsize'])
            fig_size_y = int(self.unit_data['GRAPH SIZE']['Ysize'])
        except:
            fig_size_x = FIGSIZEX
            fig_size_y = FIGSIZEY

        day_type, position_data, player_data, graph_setting = self.settingData(
            date, gtype)
        bar_type, bar_data = self.getBarData(
            position_data, player_data, graph_setting[0]['Bar'])
        line_type, line_data = self.getLineData(
            position_data, player_data, graph_setting[0]['Line'])

        # basic information
        if bar_type[0] == 'Position':
            xlabel = position_data.index
        else:
            xlabel = player_data.index

        # window setting
        fig, ax = plt.subplots(1, 1, figsize=(fig_size_x, fig_size_y))
        # fig.set_size_inches(fig_size_x, 6, forward=True)
        ax_twinx = ax.twinx()

        # draw left graph
        plotBar(ax, day_type, bar_type, bar_data,
                xlabel, wannasave, val, date, self.unit_data, line_data)
        # draw right graph
        plotLine(ax_twinx, day_type, line_type,
                 line_data, xlabel, wannasave, val, date, self.unit_data, bar_data)

        if wannasave:
            fig.tight_layout()
            title = "{}__{} graph".format(date, gtype[0])
            save_path = os.path.join(
                self.base_path, graph_path, config.IMAGE_CONFIG[gtype[0]], title+'.png')
            plt.savefig(save_path, dpi=300)
            plt.close()
            return None
        else:
            fig.set_size_inches(fig_size_y, 4)
            fig.tight_layout()
            return fig

    def makeMultiGraph(self, date, gtype, wannasave, val):
        try:
            fig_size_x = int(self.unit_data['GRAPH SIZE']['Xsize'])
            fig_size_y = int(self.unit_data['GRAPH SIZE']['Ysize'])
        except:
            fig_size_x = FIGSIZEX
            fig_size_y = FIGSIZEY

        # data setting
        day_type, position_data, player_data, graph_setting = self.settingData(
            date, gtype)

        fig_length = len(graph_setting)
        fig, ax = plt.subplots(fig_length, 1, figsize=(
            fig_size_x, fig_size_y*fig_length))
        # fig.set_size_inches(fig_size_x, 6*fig_length, forward=True)

        for gi, gt in enumerate(gtype):
            bar_type, bar_data = self.getBarData(
                position_data, player_data, graph_setting[gi]['Bar'])
            line_type, line_data = self.getLineData(
                position_data, player_data, graph_setting[gi]['Line'])

            # basic information
            if bar_type[0] == 'Position':
                xlabel = position_data.index
            else:
                xlabel = player_data.index

            # window setting
            ax_twinx = ax[gi].twinx()

            plotBar(ax[gi], day_type, bar_type, bar_data,
                    xlabel, wannasave, val, date, self.unit_data, line_data)
            # draw right graph
            plotLine(ax_twinx, day_type, line_type, line_data,
                     xlabel, wannasave, val, date, self.unit_data, bar_data)

        # graph label setting
        # plt.subplots_adjust(wspace=10.)
        fig.tight_layout()

        if wannasave:
            fig.tight_layout()
            title = "{}__{} graph".format(date, 'Total')
            save_path = os.path.join(
                self.base_path, graph_path, config.IMAGE_CONFIG['Total'], title+'.png')
            plt.savefig(save_path, dpi=300)
            plt.close()
            return None
        else:
            fig.set_size_inches(fig_size_y, 4*fig_length)
            fig.tight_layout()
            return fig

    def makeGraph(self, date, gtype, wannasave, val):
        gnum = len(gtype)
        if gnum == 0:
            fig = None
        elif gnum == 1:
            fig = self.makeSingleGraph(date, gtype, wannasave, val)
        else:
            fig = self.makeMultiGraph(date, gtype, wannasave, val)
        return fig


class PhysicoMatchGraph(PhysicoMatch):
    def __init__(self, PMANAGE):
        super().__init__(PMANAGE)
        self.unit_data = self.__loadUnitData()

    def __loadUnitData(self):
        unitdata_path = os.path.join(self.base_path, 'unit_config.conf')
        cp = configparser.ConfigParser()
        cp.read(unitdata_path)
        print(unitdata_path)
        if 'HIGHESTY' in cp.sections():
            print("success load unit data!")
            return cp
        else:
            print("fail load unit data...")
            return None

    def settingData(self, matchCamp, matchDate, matchInfo, gtype):
        matchData = super().matchTeamData(matchCamp, matchDate, matchInfo)

        day_type, position_data, player_data = matchData['type'], matchData['position'], matchData['day']

        exist_list = []
        for position in MPOSITIONLIST:
            if position in position_data.index:
                exist_list.append(position)
        position_data = position_data.reindex(index=exist_list)

        player_data['MSR %'] = player_data['MSR'] * \
            100/player_data['Total Dist.']
        player_data['HSR %'] = player_data['HSR'] * \
            100/player_data['Total Dist.']
        player_data['Sprint %'] = player_data['Sprint'] * \
            100/player_data['Total Dist.']
        player_data.loc[:, 'TR Time':] = player_data.loc[:,
                                                         'TR Time':].fillna(0)
        player_data.loc[:, 'TR Time':] = player_data.loc[:,
                                                         'TR Time':].round(1)
        player_data = player_data[player_data['Position'] != 'GK']
        player_data = player_data.set_index('Name')

        graph_setting = [MATCHGRAPHTYPE[gt] for gt in gtype]

        return day_type, position_data, player_data, graph_setting

    def getBarData(self, position_data, player_data, contentDict):
        bar_type = contentDict['wannaType']
        content_list = contentDict['needData']
        bar_dict = {}
        for (name, content) in content_list:
            if name == 'Position':
                bar_dict[content] = position_data[content]
            else:
                bar_dict[content] = player_data[content]

        return bar_type, bar_dict

    def getLineData(self, position_data, player_data, contentDict):
        line_type = contentDict['wannaType']
        content_list = contentDict['needData']
        line_dict = {}
        for (name, content) in content_list:
            if name == 'Position':
                line_dict[content] = position_data[content]
            else:
                line_dict[content] = player_data[content]

        return line_type, line_dict

    def makeSingleGraph(self, matchCamp, matchDate, matchInfo, gtype, wannasave, val):
        try:
            fig_size_x = int(self.unit_data['GRAPH SIZE']['Xsize'])
            fig_size_y = int(self.unit_data['GRAPH SIZE']['Ysize'])
        except:
            fig_size_x = FIGSIZEX
            fig_size_y = FIGSIZEY

        day_type, position_data, player_data, graph_setting = self.settingData(
            matchCamp, matchDate, matchInfo, gtype)
        bar_type, bar_data = self.getBarData(
            position_data, player_data, graph_setting[0]['Bar'])
        line_type, line_data = self.getLineData(
            position_data, player_data, graph_setting[0]['Line'])

        # basic information
        if bar_type[0] == 'Position':
            xlabel = position_data.index
        else:
            xlabel = player_data.index

        # window setting
        fig, ax = plt.subplots(1, 1, figsize=(fig_size_x, fig_size_y))
        # fig.set_size_inches(fig_size_x, 6, forward=True)
        ax_twinx = ax.twinx()

        # draw left graph
        plotBar(ax, day_type, bar_type, bar_data,
                xlabel, wannasave, val, matchDate, self.unit_data, line_data)
        # draw right graph
        plotLine(ax_twinx, day_type, line_type,
                 line_data, xlabel, wannasave, val, matchDate, self.unit_data, bar_data)

        if wannasave:
            fig.tight_layout()
            title = "{}__{}_{} graph".format(matchDate, matchInfo, gtype[0])
            save_path = os.path.join(
                self.base_path, graph_path, config.IMAGE_CONFIG[gtype[0]], title+'.png')
            plt.savefig(save_path, dpi=300)
            plt.close()
            return None
        else:
            fig.set_size_inches(fig_size_y, 4)
            fig.tight_layout()
            return fig

    def makeMultiGraph(self, matchCamp, matchDate, matchInfo, gtype, wannasave, val):
        try:
            fig_size_x = int(self.unit_data['GRAPH SIZE']['Xsize'])
            fig_size_y = int(self.unit_data['GRAPH SIZE']['Ysize'])
        except:
            fig_size_x = FIGSIZEX
            fig_size_y = FIGSIZEY

        # data setting
        day_type, position_data, player_data, graph_setting = self.settingData(
            matchCamp, matchDate, matchInfo, gtype)

        fig_length = len(graph_setting)
        fig, ax = plt.subplots(fig_length, 1, figsize=(
            fig_size_x, fig_size_y*fig_length))
        # fig.set_size_inches(fig_size_x, 6*fig_length, forward=True)

        for gi, gt in enumerate(gtype):
            bar_type, bar_data = self.getBarData(
                position_data, player_data, graph_setting[gi]['Bar'])
            line_type, line_data = self.getLineData(
                position_data, player_data, graph_setting[gi]['Line'])

            # basic information
            if bar_type[0] == 'Position':
                xlabel = position_data.index
            else:
                xlabel = player_data.index

            # window setting
            ax_twinx = ax[gi].twinx()

            plotBar(ax[gi], day_type, bar_type, bar_data,
                    xlabel, wannasave, val, matchDate, self.unit_data, line_data)
            # draw right graph
            plotLine(ax_twinx, day_type, line_type, line_data,
                     xlabel, wannasave, val, matchDate, self.unit_data, bar_data)

        # graph label setting
        # plt.subplots_adjust(wspace=10.)
        fig.tight_layout()

        if wannasave:
            fig.tight_layout()
            title = "{}__{}_{} graph".format(matchDate, matchInfo, 'Total')
            save_path = os.path.join(
                self.base_path, graph_path, config.IMAGE_CONFIG['Total'], title+'.png')
            plt.savefig(save_path, dpi=300)
            plt.close()
            return None
        else:
            fig.set_size_inches(fig_size_y, 4*fig_length)
            fig.tight_layout()
            return fig

    def makeGraph(self, matchCamp, matchDate, matchInfo, gtype, wannasave, val):
        gnum = len(gtype)
        if gnum == 0:
            fig = None
        elif gnum == 1:
            fig = self.makeSingleGraph(
                matchCamp, matchDate, matchInfo, gtype, wannasave, val)
        else:
            fig = self.makeMultiGraph(
                matchCamp, matchDate, matchInfo, gtype, wannasave, val)
        return fig
