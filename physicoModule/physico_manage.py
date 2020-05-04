import numpy as np
import pandas as pd
import copy
import os
import openpyxl
import pickle
from physicoModule import config
import physicoModule.physico_calfnc as pcf
import physicoModule.physico_subfnc as psf

# base_path = config.ROOT_CONFIG['base']
input_path = config.FOLDER_CONFIG['input']
output_path = config.FOLDER_CONFIG['output']
backup_path = config.FOLDER_CONFIG['backup']
graph_path = config.FOLDER_CONFIG['graph']
result_day = config.FILE_CONFIG['day']
result_player = config.FILE_CONFIG['player']
db_session = config.DB_CONFIG['session']
db_day = config.DB_CONFIG['dayInfo']
db_player = config.DB_CONFIG['player']
root_path = config.ROOT_CONFIG['base']


class PhysicoManage():
    FOLDERLIST = ['input', 'output', 'backup', 'graph']
    INPUTLIST = ['workout', 'wellness']
    RESULTLIST = ['day', 'player', 'match']
    IMAGELIST = ['Day Graph', 'Match Day Graph',
                 'Match Period Graph', 'Player Graph']
    WORKWELL_COLUMNS = ['dayOn', 'No.', 'Camp', 'Date', 'Name', 'Position', 'Type', 'Type Info.', 'RPE', 'TR Time', 'Total Dist.', 'Dist. per min', 'HSR+Sprint', 'MSR', 'HSR', 'Sprint',
                        'Accel Cnt.', 'Decel Cnt.', 'Max Speed', 'GPS PL', 'Load', 'Injury', 'Memo', 'Age', 'Sleep Time', 'Sleep', 'Tired', 'Stressed', 'Muscle', 'Height', 'Weight', 'Body Muscle', 'Body Fat']

    def __init__(self, base_dir):
        self.base_path = base_dir
        self.__makeDir()
        self.__makeSubDir()
        self.session_set = self.__loadDataSet('session')
        self.player_set = self.__loadDataSet('player')
        self.day_set = self.__loadDataSet('day')
        self.file_set = self.__loadDataSet('file')
        self.match_set = self.__loadDataSet('match')

    def __makeDir(self):
        for folder in self.FOLDERLIST:
            directory = os.path.join(
                self.base_path, config.FOLDER_CONFIG[folder])
            if not os.path.isdir(directory):
                os.makedirs(directory)

    def __makeSubDir(self):
        for result in self.INPUTLIST:
            directory = os.path.join(
                self.base_path, input_path, config.INPUT_CONFIG[result])
            if not os.path.isdir(directory):
                os.makedirs(directory)

        for result in self.RESULTLIST:
            directory = os.path.join(
                self.base_path, output_path, config.RESULT_CONFIG[result])
            if not os.path.isdir(directory):
                os.makedirs(directory)

        for image in self.IMAGELIST:
            directory = os.path.join(
                self.base_path, graph_path, config.IMAGE_CONFIG[image])
            if not os.path.isdir(directory):
                os.makedirs(directory)
            if image == 'Day Graph':
                sub = config.IMAGE_DAY_CONFIG
                for value in sub.values():
                    sub_dir = directory = os.path.join(
                        self.base_path, graph_path, config.IMAGE_CONFIG[image], value)
                    if not os.path.isdir(sub_dir):
                        os.makedirs(sub_dir)
            elif image == 'Match Day Graph':
                sub = config.IMAGE_MATCHDAY_CONFIG
                for value in sub.values():
                    sub_dir = directory = os.path.join(
                        self.base_path, graph_path, config.IMAGE_CONFIG[image], value)
                    if not os.path.isdir(sub_dir):
                        os.makedirs(sub_dir)
            elif image == 'Match Period Graph':
                sub = config.IMAGE_MATCHPERIOD_CONFIG
                for value in sub.values():
                    sub_dir = directory = os.path.join(
                        self.base_path, graph_path, config.IMAGE_CONFIG[image], value)
                    if not os.path.isdir(sub_dir):
                        os.makedirs(sub_dir)
            elif image == 'Player Graph':
                sub = config.IMAGE_PLAYER_CONFIG
                for value in sub.values():
                    sub_dir = directory = os.path.join(
                        self.base_path, graph_path, config.IMAGE_CONFIG[image], value)
                    if not os.path.isdir(sub_dir):
                        os.makedirs(sub_dir)

    def __loadDataSet(self, param):
        load_path = os.path.join(
            self.base_path, backup_path, config.DATA_CONFIG[param])
        try:
            with open(load_path, 'rb') as loader:
                data_dict = pickle.load(loader)
            loader.close()
        except:
            data_dict = {}
            with open(load_path, 'wb') as saver:
                pickle.dump(data_dict, saver, protocol=pickle.HIGHEST_PROTOCOL)
            saver.close()
        return data_dict

    def readSession(self, fileDate):
        # wellness data
        wellness_dict = {}
        try:
            wellness_path = os.path.join(
                self.base_path, input_path, config.INPUT_CONFIG['wellness'], '{}.xlsx'.format(fileDate+'_WEL'))
            well_xl = pd.ExcelFile(wellness_path)
            for i, sn in enumerate(well_xl.sheet_names):
                if i == 0:
                    well_info = well_xl.parse(sn)
                elif i == 1:
                    well_data = well_xl.parse(sn).drop(['No.'], axis=1)
                else:
                    raise("wellness file error")
            wellness_dict[fileDate] = {
                'well_info': well_info, 'well_data': well_data}
        except:
            raise("wellness file doesn't exist!!!")
        camp = well_info['Camp'].values[0]

        # workout data
        workout_path = os.path.join(
            self.base_path, input_path, config.INPUT_CONFIG['workout'])
        file_list = [x.split('.')[0] for x in os.listdir(workout_path)]
        target_list = []
        for file in file_list:
            if file.split('_')[0] == fileDate:
                target_list.append(file)
        file_names = []
        for file in target_list:
            if file.split('_')[1] == 'TR':
                file_names.append('TR')
            else:
                file_names.append(file.split('_')[1])
        tr_session = []
        match_session = []
        for file_name in file_names:
            file_date, file_type = fileDate, file_name
            data_path = os.path.join(
                workout_path, '{}_{}.xlsx'.format(file_date, file_type))
            xl = pd.ExcelFile(data_path)
            if file_type == 'TR':
                for i, sn in enumerate(xl.sheet_names):
                    tr_session.append(sn)
                    data = xl.parse(sn)
                    data['Load'] = data['RPE'] * data['TR Time']
                    # data = data.rename(columns={'RPE': 'RPE_{}'.format(i+1)})
                    file_info = ('TR', sn)
                    try:
                        self.session_set[file_date][file_info] = data
                    except:
                        self.session_set[file_date] = {}
                        self.session_set[file_date][file_info] = data
            else:
                match_session.append(file_type)
                data_dict = {}
                for i, sn in enumerate(xl.sheet_names):
                    data = xl.parse(sn)
                    if i == 0:
                        part = 'First Half'
                    elif i == 1:
                        part = 'Second Half'
                    else:
                        part = 'Extra Time'
                    data_dict[part] = data
                    data_dict[part]['Load'] = data_dict[part]['RPE'] * \
                        data_dict[part]['TR Time']

                    match = data.loc[:, 'TR Time':]
                    if i == 0:
                        match_info = data.loc[:, :'RPE']
                        match_data = match.values
                        max_speed = match['Max Speed'].values
                        columns = match.columns
                    else:
                        match_data = psf.sumNanNum(match_data, match.values)
                        max_speed = psf.getMax(
                            max_speed, match['Max Speed'].values)

                match_df = pd.DataFrame(match_data, columns=columns)
                match_df['Max Speed'] = pd.Series(max_speed)
                match_df = match_df.round(1)
                # merge info, rpe, data
                match_df = pd.concat([match_info, match_df], axis=1)

                match_basic_info = (camp, file_date, file_type)
                self.match_set[match_basic_info] = data_dict

                # Write match DB ####################################################################################
                match_dff = pd.DataFrame(columns=['Camp', 'Date', 'Against', 'Part',
                                                  'No.', 'Name', 'Position', 'Type', 'Type Info.', 'RPE', 'TR Time',
                                                  'Total Dist.', 'Dist. per min', 'HSR+Sprint', 'MSR',
                                                  'HSR', 'Sprint', 'Accel Cnt.', 'Decel Cnt.',
                                                  'Max Speed', 'GPS PL', 'Injury', 'Memo', 'Load'])
                match_dict = copy.deepcopy(data_dict)
                for key, value in match_dict.items():
                    value['Part'] = key
                    value['Camp'] = camp
                    value['Date'] = file_date
                    value['Against'] = file_type
                    match_dff = match_dff.append(
                        value, sort=False, ignore_index=True)

                match_db_path = os.path.join(root_path, 'physico_db',
                                             config.DB_CONFIG['match'])
                with open(match_db_path, 'rb') as loader:
                    match_db = pickle.load(loader)
                loader.close()
                match_db = match_db.append(
                    match_dff, sort=False, ignore_index=True)
                match_db = match_db.drop_duplicates(
                    ['Camp', 'Date', 'Against', 'Part', 'Name'], keep='last')
                with open(match_db_path, 'wb') as saver:
                    pickle.dump(match_db, saver,
                                protocol=pickle.HIGHEST_PROTOCOL)
                saver.close()
                ##################################################################################################

                file_info = ('M', file_type)
                try:
                    self.session_set[file_date][file_info] = match_df
                except:
                    self.session_set[file_date] = {}
                    self.session_set[file_date][file_info] = match_df

        # write daily workout type
        self.file_set[file_date] = {'Camp': camp,
                                    'TR': tr_session, 'M': match_session}

        # Session DB #########################################################################################
        session_df = pd.DataFrame(columns=['Camp', 'Date', 'Session', 'Session Title', 'No.', 'Name', 'Position', 'Type', 'Type Info.', 'RPE', 'TR Time', 'Total Dist.',
                                           'Dist. per min', 'HSR+Sprint', 'MSR', 'HSR', 'Sprint', 'Accel Cnt.', 'Decel Cnt.', 'Max Speed', 'GPS PL', 'Injury', 'Memo', 'Load'])
        session_data = copy.deepcopy(self.session_set[file_date])
        for key, value in session_data.items():
            session_value = value
            session_value['Camp'] = camp
            session_value['Date'] = file_date
            session_value['Session'] = key[0]
            session_value['Session Title'] = key[1]
            session_df = session_df.append(
                session_value, sort=False, ignore_index=True)

        # Wellness DB ###########################################################################################
        wellness_df = pd.DataFrame(columns=['Camp', 'Date', 'Weather', 'High Temp.', 'Low Temp.', 'Humidity', 'Name',
                                            'Age', 'Sleep Time', 'Sleep', 'Tired', 'Stressed', 'Muscle', 'Height', 'Weight', 'Body Muscle', 'Body Fat'])
        wellness_df = wellness_df.append(
            well_data, sort=False, ignore_index=True)
        wellness_df[well_info.columns] = well_info.values[0]
        # session_dict[file_date] = self.session_set[file_date]

        # Write session DB
        session_db_path = os.path.join(root_path, 'physico_db',
                                       config.DB_CONFIG['session'])
        with open(session_db_path, 'rb') as loader:
            session_db = pickle.load(loader)
        loader.close()
        session_db = session_db.append(
            session_df, sort=False, ignore_index=True)
        session_db = session_db.drop_duplicates(
            ['Camp', 'Date', 'Session', 'Session Title', 'Name'], keep='last')
        with open(session_db_path, 'wb') as saver:
            pickle.dump(session_db, saver, protocol=pickle.HIGHEST_PROTOCOL)
        saver.close()

        wellness_db_path = os.path.join(root_path, 'physico_db',
                                        config.DB_CONFIG['wellness'])
        with open(wellness_db_path, 'rb') as loader:
            wellness_db = pickle.load(loader)
        loader.close()
        wellness_db = wellness_db.append(
            wellness_df, sort=False, ignore_index=True)
        wellness_db = wellness_db.drop_duplicates(
            ['Camp', 'Date', 'Name', 'Age'], keep='last')
        with open(wellness_db_path, 'wb') as saver:
            pickle.dump(wellness_db, saver, protocol=pickle.HIGHEST_PROTOCOL)
        saver.close()

        return self.session_set[file_date], well_info, well_data

    def mergeData(self, rData, wInfo):
        for i, value in enumerate(rData.values()):
            tdata = value[(value['Type'] == 'F') | (value['Type'] == 'M') | (
                value['Type'] == 'IN') | (value['Type'] == 'G')]
            session_name = list(tdata['Name'].values)
            data = value.loc[:, 'TR Time':]
            if i == 0:
                unique_name = session_name
                # player information
                merged_info = value.loc[:, :'RPE']
                # Data
                merged_data = data.values
                columns = data.columns
                max_speed = data['Max Speed'].values
            else:
                for name in unique_name:
                    if not name in session_name:
                        unique_name.append(name)
                # Type
                merged_info['Type'] = psf.sumNanStr(
                    merged_info['Type'], value['Type'])
                merged_info['Type Info.'] = psf.sumNanStr(
                    merged_info['Type Info.'], value['Type Info.'])
                merged_info['RPE'] = psf.sumNanStr(
                    merged_info['RPE'], value['RPE'])
                merged_data = psf.sumNanNum(merged_data, data.values)
                max_speed = psf.getMax(
                    max_speed, data['Max Speed'].values)

        merged_data = pd.DataFrame(merged_data, columns=columns)
        merged_data['Max Speed'] = pd.Series(max_speed)
        merged_data = merged_data.round(1)
        # merge info, data
        merged_df = pd.concat([merged_info, merged_data], axis=1)
        merged_df['dayOn'] = merged_df.Name.apply(lambda x: x in unique_name)
        workout_date = str(wInfo['Date'].values[0])
        self.file_set[workout_date]['Player'] = unique_name

        # Write dayInfo DB
        db_data = self.file_set[workout_date]
        db_data = pd.DataFrame([db_data.values()], columns=db_data.keys())
        db_data['Date'] = workout_date

        db_path = os.path.join(root_path, 'physico_db',
                               config.DB_CONFIG['dayInfo'])
        with open(db_path, 'rb') as loader:
            dayInfo_db = pickle.load(loader)
        loader.close()
        dayInfo_db = dayInfo_db.append(db_data, sort=False, ignore_index=True)
        dayInfo_db = dayInfo_db.drop_duplicates(['Camp', 'Date'], keep='last')
        with open(db_path, 'wb') as saver:
            pickle.dump(dayInfo_db, saver, protocol=pickle.HIGHEST_PROTOCOL)
        saver.close()

        return unique_name, merged_df

    # combine workout + well
    def combineWellness(self, mData, wInfo, wData):
        workwell = pd.merge(left=mData, right=wData,
                            how='left', on=['Name'], sort=False)
        workwell['Camp'] = wInfo['Camp'].values[0]
        workwell['Date'] = wInfo['Date'].values[0]
        workwell['Weather'] = wInfo['Weather'].values[0]
        workwell['High Temp.'] = wInfo['High Temp.'].values[0]
        workwell['Low Temp.'] = wInfo['Low Temp.'].values[0]
        workwell['Humidity'] = wInfo['Humidity'].values[0]
        workwell = workwell[self.WORKWELL_COLUMNS]

        # Write DB
        db_path = os.path.join(root_path, 'physico_db',
                               config.DB_CONFIG['player'])
        with open(db_path, 'rb') as loader:
            player_db = pickle.load(loader)
        loader.close()
        player_db = player_db.append(workwell, sort=False, ignore_index=True)
        player_db = player_db.drop_duplicates(
            ['Camp', 'Date', 'Name'], keep='last')
        with open(db_path, 'wb') as saver:
            pickle.dump(player_db, saver, protocol=pickle.HIGHEST_PROTOCOL)
        saver.close()

        return workwell

    ###################################################################################################################
    # for each player and team
    def makeTeamData(self, uniqueName, mData):
        tData = mData.set_index('Name').loc[uniqueName, :]
        position_df = tData.drop(
            columns=['No.', 'Date', 'Type']).groupby('Position').mean()

        tData = tData[tData['Position'] != 'GK']
        team = tData.loc[:, 'TR Time':]
        team_df = pd.DataFrame([team.mean()], columns=team.columns)
        team_df = team_df.round(1)
        team_df['Name'] = 'Team'
        team_df['Date'] = mData['Date'].mean()
        try:
            team_df['Camp'] = mData['Camp'].value_counts().index[0]
        except:
            team_df['Camp'] = None
        try:
            team_df['Type'] = mData['Type'].value_counts().index[0]
        except:
            team_df['Type'] = None
        try:
            team_df['Type Info.'] = mData['Type Info.'].value_counts().index[0]
        except:
            team_df['Type Info.'] = None
        merged_df = mData.append(team_df, sort=False, ignore_index=True)
        merged_df['Date'] = merged_df['Date'].astype(int)

        position_df = position_df.append(team_df.set_index('Name').drop(
            columns=['Camp', 'Date', 'Type']), sort=False)
        position_df = position_df.round(1)
        fileInfo = str(int(mData['Date'].mean()))
        self.day_set[fileInfo] = {}
        self.day_set[fileInfo]['Player'] = uniqueName
        self.day_set[fileInfo]['Data'] = position_df
        return position_df, merged_df

    def makePlayerData(self, mData):
        raw_data = mData.set_index('Name')
        if self.player_set:
            player = raw_data
            for name in player.index:
                data = player.loc[name:name, :]
                # make new player key
                if not name in self.player_set.keys():
                    team_shape = self.player_set['Team'].values.shape
                    team_columns = self.player_set['Team'].columns
                    copy_m = np.full(team_shape, np.NaN)
                    copy_df = pd.DataFrame(copy_m, columns=team_columns, index=[
                                           name for i in range(team_shape[0])])
                    copy_df['Date'] = self.player_set['Team']['Date'].values
                    self.player_set[name] = copy_df
                # append new data on db data
                self.player_set[name] = self.player_set[name].append(
                    data, sort=False)
        # firt data_set
        else:
            for name in raw_data.index:
                self.player_set[name] = raw_data.loc[name:name, :]
        return None

    ###################################################################################################################
    ###################################################################################################################
    # to save
    def saveDataSet(self, dataset, param):
        save_path = os.path.join(
            self.base_path, backup_path, config.DATA_CONFIG[param])
        with open(save_path, 'wb') as saver:
            pickle.dump(dataset, saver,
                        protocol=pickle.HIGHEST_PROTOCOL)
        saver.close()
        return None

    def updateManager(self):
        dir_path = os.path.join(self.base_path, input_path,
                                config.INPUT_CONFIG['workout'])
        file_list = [x.split('.')[0].split('_')[0]
                     for x in os.listdir(dir_path)]
        file_list = list(set(file_list))
        file_list.sort()
        todo_list = []
        for file in file_list:
            if not file in self.file_set.keys():
                todo_list.append(file)
        for file_name in todo_list:
            file_str = file_name.split('_')[0]
            if len(file_str) == 8:
                date = int(file_str)
                rData, wInfo, wData = self.readSession(file_name)
                tname, mData = self.mergeData(rData, wInfo)
                wData = self.combineWellness(mData, wInfo, wData)
                pData, tData = self.makeTeamData(tname, wData)

                self.makePlayerData(tData)
                self.saveDataSet(self.session_set, 'session')
                self.saveDataSet(self.player_set, 'player')
                self.saveDataSet(self.day_set, 'day')
                self.saveDataSet(self.file_set, 'file')
                self.saveDataSet(self.match_set, 'match')
        return todo_list
