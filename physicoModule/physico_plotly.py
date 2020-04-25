import numpy as np
import pandas as pd
import os
import openpyxl
import plotly as py
import plotly.graph_objects as go
from physicoModule import config
from physicoModule.physico_control import PhysicoControl

graph_path = config.FOLDER_CONFIG['graph']


class PhysicoPlotly(PhysicoControl):
    def __init__(self, PMANAGE):
        super().__init__(PMANAGE)
        self.data_df = self.__receiveData()

    def __receiveData(self):
        player_gdict = self.player_set
        team_gdata = self.player_set['Team']
        df = pd.DataFrame()
        for key, value in self.player_set.items():
            df = df.append(value, sort=False)
        df['DateTime'] = pd.to_datetime(
            df['Date'].astype(str), format='%Y%m%d')
        return df

    def makeSinglePlotly(self, name):
        name_df = self.data_df.query("Name=='{}'".format(name))
        fig = go.Figure(data=[go.Scatter(
            x=name_df['DateTime'],
            y=name_df['Load'],
            mode='markers',
            marker=dict(
                sizemin=5
            )
        )])
        fig.show()
