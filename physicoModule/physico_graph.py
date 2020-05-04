import numpy as np
import pandas as pd
import os
import openpyxl
import configparser
from physicoModule import config
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from physicoModule.physico_control import PhysicoControl, PhysicoMatch
from physicoModule.physico_plotset import PLAYERGRAPHTYPE, DAYGRAPHTYPE, MATCHGRAPHTYPE, MATCHPERIODGRAPHTYPE
from physicoModule.physico_plotfnc import HIGHESTY, TRPOSITIONLIST, MPOSITIONLIST
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
                self.base_path, graph_path, config.IMAGE_CONFIG['Player Graph'], config.IMAGE_PLAYER_CONFIG[gtype[0]], title+'.png')
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
                self.base_path, graph_path, config.IMAGE_CONFIG['Player Graph'], config.IMAGE_PLAYER_CONFIG['Total'], title+'.png')
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
        player_df = player_df.round(1)
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
                self.base_path, graph_path, config.IMAGE_CONFIG['Day Graph'], config.IMAGE_DAY_CONFIG[gtype[0]], title+'.png')
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
                self.base_path, graph_path, config.IMAGE_CONFIG['Day Graph'], config.IMAGE_DAY_CONFIG['Total'], title+'.png')
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
    position_columns = ['TR Time', 'Total Dist.', 'Dist. per min',
                        'MSR', 'HSR', 'Sprint', 'Accel Cnt.', 'Decel Cnt.']
    position_sumcol = ['TR Time <SUM>', 'Total Dist. <SUM>', 'Dist. per min <SUM>',
                       'MSR <SUM>', 'HSR <SUM>', 'Sprint <SUM>', 'Accel Cnt. <SUM>', 'Decel Cnt. <SUM>']

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
        matchData, fh, sh = super().matchTeamData(matchCamp, matchDate, matchInfo)

        day_type, position_data, player_data = matchData['type'], matchData['position'], matchData['day']

        exist_list = []
        for position in MPOSITIONLIST:
            if position in position_data.index:
                exist_list.append(position)
        position_data = position_data.reindex(index=exist_list)
        position_data = position_data.round(1)

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

        # Full Time player Data
        full_time = player_data[(player_data['TR Time'] >= 90) & (
            player_data['Position'] != 'GK')]
        position_avg = full_time.groupby('Position').mean().round(1)[
            self.position_columns]
        exist_list = []
        for position in TRPOSITIONLIST:
            if position in position_avg.index:
                exist_list.append(position)
        position_avg = position_avg.reindex(index=exist_list).round(1)

        # All Position Player Data
        ft = fh[(fh.Type == 'M') & (fh.Position != 'GK') & (
            fh.Position != 'R')].groupby('Position').sum()[self.position_columns]
        st = sh[(sh.Type == 'M') & (sh.Position != 'GK') & (
            sh.Position != 'R')].groupby("Position").sum()[self.position_columns]
        ft.columns = self.position_sumcol
        st.columns = self.position_sumcol
        position_index = ft.index.append(st.index).unique()
        position_list = []
        for position in TRPOSITIONLIST:
            if position in position_index:
                position_list.append(position)
        position_sum = ft.reindex(index=position_list).add(
            st.reindex(index=position_list), fill_value=0).round(1)

        player_data = player_data.set_index(
            ['Position', player_data.index]).reindex(index=position_list, level=0)
        player_data = player_data.round(1)

        graph_setting = [MATCHGRAPHTYPE[gt] for gt in gtype]

        return day_type, position_data, position_avg, position_sum, player_data, graph_setting

    def getBarData(self, position_data, position_avg, position_sum, player_data, contentDict):
        bar_type = contentDict['wannaType']
        content_list = contentDict['needData']
        bar_dict = {}
        for (name, content) in content_list:
            if name == 'Position':
                bar_dict[content] = position_data[content]
            elif name == 'Position Average':
                bar_dict[content] = position_avg[content]
            elif name == 'Position Sum':
                bar_dict[content] = position_sum[content]
            else:
                bar_dict[content] = player_data[content]

        return bar_type, bar_dict

    def getLineData(self, position_data, position_avg, position_sum, player_data, contentDict):
        line_type = contentDict['wannaType']
        content_list = contentDict['needData']
        line_dict = {}
        for (name, content) in content_list:
            if name == 'Position':
                line_dict[content] = position_data[content]
            elif name == 'Position Average':
                line_dict[content] = position_avg[content]
            elif name == 'Position Sum':
                line_dict[content] = position_sum[content]
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

        day_type, position_data, position_avg, position_sum, player_data, graph_setting = self.settingData(
            matchCamp, matchDate, matchInfo, gtype)
        bar_type, bar_data = self.getBarData(
            position_data, position_avg, position_sum, player_data, graph_setting[0]['Bar'])
        line_type, line_data = self.getLineData(
            position_data, position_avg, position_sum, player_data, graph_setting[0]['Line'])

        # basic information
        if bar_type[0] == 'Position':
            xlabel = position_data.index
        elif bar_type[0] == 'Position Average':
            xlabel = position_avg.index
        elif bar_type[0] == 'Position Sum':
            xlabel = position_sum.index
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
                self.base_path, graph_path, config.IMAGE_CONFIG['Match Day Graph'], config.IMAGE_MATCHDAY_CONFIG[gtype[0]], title+'.png')
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
        day_type, position_data, position_avg, position_sum, player_data, graph_setting = self.settingData(
            matchCamp, matchDate, matchInfo, gtype)

        fig_length = len(graph_setting)
        fig, ax = plt.subplots(fig_length, 1, figsize=(
            fig_size_x, fig_size_y*fig_length))
        # fig.set_size_inches(fig_size_x, 6*fig_length, forward=True)

        for gi, gt in enumerate(gtype):
            bar_type, bar_data = self.getBarData(
                position_data, position_avg, position_sum, player_data, graph_setting[gi]['Bar'])
            line_type, line_data = self.getLineData(
                position_data, position_avg, position_sum, player_data, graph_setting[gi]['Line'])

            # basic information
            if bar_type[0] == 'Position':
                xlabel = position_data.index
            elif bar_type[0] == 'Position Average':
                xlabel = position_avg.index
            elif bar_type[0] == 'Position Sum':
                xlabel = position_sum.index
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
                self.base_path, graph_path, config.IMAGE_CONFIG['Match Day Graph'], config.IMAGE_MATCHDAY_CONFIG['Total'], title+'.png')
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


class PhysicoMatchPeriodGraph(PhysicoMatch):
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

    def settingData(self, matchCamp, matchDate, matchInfo, befor_period, after_period, gtype):
        period_col = ['Total Dist.', 'MSR', 'HSR', 'Sprint',
                      'Accel Cnt.', 'Decel Cnt.', 'GPS PL', 'Load']
        # match d-1
        # pre_day = datetime.strptime(matchDate, '%Y%m%d') - timedelta(days=1)
        # pre_day = datetime.strftime(pre_day, '%Y%m%d')
        # print(pre_day)

        # fixed range
        befor_day = datetime.strptime(
            matchDate, '%Y%m%d') - timedelta(days=befor_period)
        befor_day = int(datetime.strftime(befor_day, '%Y%m%d'))
        after_day = datetime.strptime(
            matchDate, '%Y%m%d') + timedelta(days=after_period)
        after_day = int(datetime.strftime(after_day, '%Y%m%d'))

        # load match day data
        matchData, _, _ = super().matchTeamData(matchCamp, matchDate, matchInfo)

        day_type, position_data, player_data = matchData['type'], matchData['position'], matchData['day']

        # match team data
        match_df = position_data.loc['Total Avg.', :]
        match_data = match_df[period_col]
        # on-field player data
        player_data = player_data[(player_data['Position'] != 'R') & (
            player_data['Position'] != 'GK')]
        # on-field player name
        player_name = player_data['Name'].values

        on_player_df = pd.DataFrame()
        off_player_df = pd.DataFrame()
        for name in self.player_set.keys():
            if name in player_name:
                data = self.player_set[name]
                data = data.reset_index()
                on_player_df = on_player_df.append(
                    data, sort=False, ignore_index=True)
            elif name == 'Team':
                pass
            else:
                data = self.player_set[name]
                data = data.reset_index()
                off_player_df = off_player_df.append(
                    data, sort=False, ignore_index=True)

        off_player_df = off_player_df[off_player_df['dayOn']]
        off_player_df = off_player_df[off_player_df['Position'] != 'GK']

        on_player_df = on_player_df[on_player_df['dayOn']]
        on_player_df = on_player_df[on_player_df['Position'] != 'GK']

        on_df = on_player_df.groupby('Date').mean()[period_col]
        off_df = off_player_df.groupby('Date').mean()[period_col]

        team_df = self.player_set['Team']
        team_df = team_df.set_index('Date')[period_col]

        team_df.loc[int(matchDate), :] = match_data
        on_df.loc[int(matchDate), :] = match_data
        # off_df.loc[int(matchDate),:] = match_data

        on_df.columns = ['{}:On'.format(col) for col in on_df.columns]
        off_df.columns = ['{}:Off'.format(col) for col in off_df.columns]
        # team_df.columns = ['Team_{}'.format(col) for col in team_df.columns]

        period_data = pd.concat([team_df, on_df, off_df], axis=1).round(1)

        period_data = period_data.loc[befor_day:after_day, :]
        period_data = period_data.rename(index={int(matchDate): 'Match Day'})
        period_data = period_data.round(1)
        graph_setting = [MATCHPERIODGRAPHTYPE[gt] for gt in gtype]

        return day_type, period_data, graph_setting

    def getBarData(self, period_data, contentDict):
        bar_type = contentDict['wannaType']
        content_list = contentDict['needData']
        bar_dict = {}
        for (name, content) in content_list:
            bar_dict[content] = period_data[content]

        return bar_type, bar_dict

    def getLineData(self, period_data, contentDict):
        line_type = contentDict['wannaType']
        content_list = contentDict['needData']
        line_dict = {}
        for (name, content) in content_list:
            line_dict[content] = period_data[content]

        return line_type, line_dict

    def makeSingleGraph(self, matchCamp, matchDate, matchInfo, befor_period, after_period, gtype, wannasave, val):
        try:
            fig_size_x = int(self.unit_data['GRAPH SIZE']['Xsize'])
            fig_size_y = int(self.unit_data['GRAPH SIZE']['Ysize'])
        except:
            fig_size_x = FIGSIZEX
            fig_size_y = FIGSIZEY

        day_type, period_data, graph_setting = self.settingData(
            matchCamp, matchDate, matchInfo, befor_period, after_period, gtype)
        bar_type, bar_data = self.getBarData(
            period_data, graph_setting[0]['Bar'])
        line_type, line_data = self.getLineData(
            period_data, graph_setting[0]['Line'])

        # basic information
        xlabel = period_data.index

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
                self.base_path, graph_path, config.IMAGE_CONFIG['Match Period Graph'], config.IMAGE_MATCHPERIOD_CONFIG[gtype[0]], title+'.png')
            plt.savefig(save_path, dpi=300)
            plt.close()
            return None
        else:
            fig.set_size_inches(fig_size_y, 4)
            fig.tight_layout()
            return fig

    def makeMultiGraph(self, matchCamp, matchDate, matchInfo, befor_period, after_period, gtype, wannasave, val):
        try:
            fig_size_x = int(self.unit_data['GRAPH SIZE']['Xsize'])
            fig_size_y = int(self.unit_data['GRAPH SIZE']['Ysize'])
        except:
            fig_size_x = FIGSIZEX
            fig_size_y = FIGSIZEY

        # data setting
        day_type, period_data, graph_setting = self.settingData(
            matchCamp, matchDate, matchInfo, befor_period, after_period, gtype)

        fig_length = len(graph_setting)
        fig, ax = plt.subplots(fig_length, 1, figsize=(
            fig_size_x, fig_size_y*fig_length))
        # fig.set_size_inches(fig_size_x, 6*fig_length, forward=True)

        for gi, gt in enumerate(gtype):
            bar_type, bar_data = self.getBarData(
                period_data, graph_setting[gi]['Bar'])
            line_type, line_data = self.getLineData(
                period_data, graph_setting[gi]['Line'])

            # basic information
            xlabel = period_data.index

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

    def makeGraph(self, matchCamp, matchDate, matchInfo, befor_period, after_period, gtype, wannasave, val):
        gnum = len(gtype)
        if gnum == 0:
            fig = None
        elif gnum == 1:
            fig = self.makeSingleGraph(
                matchCamp, matchDate, matchInfo, befor_period, after_period, gtype, wannasave, val)
        else:
            fig = self.makeMultiGraph(
                matchCamp, matchDate, matchInfo, befor_period, after_period, gtype, wannasave, val)
        return fig
