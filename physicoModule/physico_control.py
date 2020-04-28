import numpy as np
import pandas as pd
import os
import openpyxl
import pickle
from physicoModule import config
import physicoModule.physico_calfnc as pcf
import physicoModule.physico_subfnc as psf


class PhysicoControl():
    POSITIONLIST = ['GK', 'CB', 'SB', 'FB', 'CMF',
                    'DMF', 'AMF', 'MF', 'WF', 'FW', 'Team', '1st Half', '2nd Half', 'Total', 'Reserve_Tot.']

    def __init__(self, PMANAGE):
        self.base_path = PMANAGE.base_path
        self.file_set = PMANAGE.file_set
        self.player_set = PMANAGE.player_set
        self.day_set = PMANAGE.day_set
        self.__calculateAcc()
        self.player_excel = {}
        self.day_excel = {}

    def __calculateAcc(self):
        for key, value in self.player_set.items():
            # value.loc[:, 'RPE_1'] = value.loc[:, 'RPE_1'].fillna(0.)
            load = value['Load']
            mono = pcf.calculateMono(load)
            value['Mono'] = mono.round(1)
            value['Strain'] = pcf.calculateStrain(load, mono)
            value['EWAM'] = pcf.calculateEwam(load)
            value['Weight Change'] = value['Weight'].pct_change(
                fill_method='ffill').fillna(0)
            value['Weight Change'] = value['Weight Change']*100
            value['MSR %'] = value['MSR']*100/value['Total Dist.']
            value['HSR %'] = value['HSR']*100/value['Total Dist.']
            value['Sprint %'] = value['Sprint']*100/value['Total Dist.']
            value.loc[:, 'TR Time':] = value.loc[:,
                                                 'TR Time':].round(1)

    def makePlayerExcelData(self):
        for key, value in self.player_set.items():
            data = value.loc[:, 'TR Time':]
            mean_df = pd.DataFrame([data.mean()], columns=data.columns)
            mean_df = mean_df.round(1)
            mean_df['Date'] = 'Total'
            total_df = value.append(mean_df, sort=False, ignore_index=True)
            self.player_excel[key] = total_df.drop(['No.', 'Position'], axis=1)
        return self.player_excel

    def makeDayExcelData(self, date):
        # make datafrmae
        team_df = self.player_set['Team']
        team_df = team_df[team_df['Date'] == date]
        day_df = pd.DataFrame(columns=team_df.columns)

        for key, value in self.player_set.items():
            player_df = value[value['Date'] == date]
            day_df = day_df.append(player_df, sort=False)
        day_df = day_df.drop('Team')
        day_df.insert(1, 'Name', day_df.index)
        day_df = day_df.sort_values(by='No.', axis=0)
        day_df['No.'] = day_df['No.'].astype(int)
        day_df.index = pd.RangeIndex(1, len(day_df)+1)

        position_df = self.day_set[str(date)]['Data']
        position_list = []
        for position in self.POSITIONLIST:
            if position in position_df.index:
                position_list.append(position)
        position_df = position_df.reindex(index=position_list)
        position_df = position_df.reset_index()
        position_df = position_df.rename(columns={'index': 'Position'})

        self.day_excel['type'] = 'TR'
        self.day_excel['position'] = position_df
        self.day_excel['day'] = day_df
        return self.day_excel


class PhysicoMatch():
    def __init__(self, PMANAGE):
        self.base_path = PMANAGE.base_path
        self.match_set = PMANAGE.match_set

    def matchTeamData(self, matchCamp, matchDate, matchInfo):
        match_excel = {}
        match_session = self.match_set[(matchCamp, matchDate, matchInfo)]

        for i, value in enumerate(match_session.values()):
            match = value.loc[:, 'TR Time':]
            if i == 0:
                first_half = value[value['Type'] == 'M']
                match_info = value.loc[:, :'RPE']
                match_data = match.values
                max_speed = match['Max Speed'].values
                columns = match.columns
            else:
                if i == 1:
                    second_half = value[value['Type'] == 'M']
                else:
                    extra_half = value[value['Type'] == 'M']
                match_data = psf.sumNanNum(match_data, match.values)
                max_speed = psf.getMax(
                    max_speed, match['Max Speed'].values)
        match_df = pd.DataFrame(match_data, columns=columns)
        match_df['Max Speed'] = pd.Series(max_speed)
        match_df = match_df.round(1)
        # merge info, rpe, data
        match_df = pd.concat([match_info, match_df], axis=1)
        match_df = match_df[match_df['Type'] == 'M']

        first_total, first_len = pcf.calculateTotal(
            first_half, 'M', '1st Half')
        first_avg = pcf.calculateAverage(first_total, 10, '1st Half Avg.')

        second_total, second_len = pcf.calculateTotal(
            second_half, 'M', '2nd Half')
        second_avg = pcf.calculateAverage(
            second_total, 10, '2nd Half Avg.')

        day_total, day_len = pcf.calculateTotal(match_df, 'M', 'Total')
        day_avg = pcf.calculateAverage(day_total, 10, 'Total Avg.')

        reserve_total, reserve_len = pcf.calculateTotal(
            match_df, 'R', 'Reserve Tot.')
        reserve_avg = pcf.calculateAverage(
            reserve_total, reserve_len, 'Reserve Avg.')

        position_df = pd.DataFrame()
        position_df = position_df.append(first_total, sort=False)
        position_df = position_df.append(first_avg, sort=False)
        position_df = position_df.append(second_total, sort=False)
        position_df = position_df.append(second_avg, sort=False)
        position_df = position_df.append(day_total, sort=False)
        position_df = position_df.append(day_avg, sort=False)
        position_df = position_df.append(reserve_total, sort=False)
        position_df = position_df.append(reserve_avg, sort=False)
        position_df = position_df.round(1)
        position_df.insert(0, 'Type Info.', matchInfo)
        position_df.insert(0, 'Type', 'M')
        position_df.insert(0, 'Date', matchDate)
        position_df.insert(0, 'Camp', matchCamp)
        position_df.insert(0, 'Position', position_df.index)

        match_excel['type'] = 'M'
        match_excel['position'] = position_df
        match_excel['day'] = match_df

        # first_half, second_half 를 이용하여 -> posiotion 별 데이터 봅아내기

        return match_excel
