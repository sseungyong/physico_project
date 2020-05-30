import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from physicoModule.physico_plotset import PLAYERGRAPHTYPE, DAYGRAPHTYPE, MATCHGRAPHTYPE, MATCHPERIODGRAPHTYPE
from physicoModule.physico_plotunit import GRAPHUNIT, HIGHESTY, LOWESTY

font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
font_set = [(f.name, f.fname)
            for f in fm.fontManager.ttflist if ('Nanum' in f.name) | ('HY' in f.name) | ('Apple' in f.name)]
font = font_set[3]
font_name = font[0]
matplotlib.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

DEFAULTBARCOLOR = {'0': 'y', '1': 'b', '2': 'r', '3': 'k'}
DEFAULTLINECOLOR = {'0': 'k', '1': 'g', '2': 'm', '3': 'r'}
DEFAULTMARKER = 's'
DEFAULTLINESTYLE = '--'
DEFAULTSCATTERSIZE = 50
DEFAULTBARALPHA = 0.4

TRPOSITIONLIST = ['CB', 'SB', 'FB', 'CMF',
                  'DMF', 'AMF', 'MF', 'WF', 'FW', 'Team']
MPOSITIONLIST = ['1st Half Avg.',
                 '2nd Half Avg.', 'Total Avg.', 'Reserve Avg.']

FIVELEVEL_ANNOTATION = ['PG_Sleep', 'PG_Muscle',
                        'DG_Player Sleep', 'DG_Player Muscle']
WEIGHT_ANNOTATION = ['PG_Player Weight', 'DG_Player Weight']
MONOSTRAIN_ANNOTATION = ['PG_Mono & Strain', 'DG_Player Mono & Strain']
BAR_ANNOTATION = ['PG_Distance', 'PG_Load', 'PG_Dist. Load', 'PG_Mono & Strain', 'PG_MSR', 'PG_HSR', 'PG_Sprint',
                  'PG_Accel, Decel', 'PG_Max Speed', 'PG_Body Index',
                  'DG_Position Distance', 'DG_Player Distance', 'DG_Player MSR', 'DG_Player HSR', 'DG_Player Sprint',
                  'DG_Player Mono & Strain', 'DG_Player Accel, Decel', 'DG_Player Total Time & Dist.', 'DG_Player Total Time & HSR', 'DG_Player Total Time & Sprint',
                  'MG_Team Time Distance', 'MG_Position Average Distance', 'MG_Position Sum Distance', 'MG_Player Distance', 'MG_Player Total Time & Dist.',
                  'MG_Player Total Time & HSR', 'MG_Player Total Time & Sprint', 'MG_Player Total Time & Dist. per min', 'MG_Player Accel, Decel',
                  'PM_Player Distance', 'PM_Player Accel, Decel', 'PM_Player Load']
LINE_ANNOTATION = ['PG_Load', 'PG_Dist. Load', 'PG_Body Index',
                   'DG_Position Distance', 'DG_Player MSR', 'DG_Player HSR', 'DG_Player Sprint', 'DG_Player Total Time & Dist.',
                   'DG_Player Total Time & HSR', 'DG_Player Total Time & Sprint',
                   'MG_Team Time Distance', 'MG_Position Average Distance', 'MG_Position Sum Distance', 'MG_Player Distance', 'MG_Player Total Time & Dist.',
                   'MG_Player Total Time & HSR', 'MG_Player Total Time & Sprint', 'MG_Player Total Time & Dist. per min', 'MG_Player Accel, Decel',
                   'PM_Player Distance', 'PM_Player Accel, Decel', 'PM_Player Load']
# Parameters
DEFAULTtitle_font = 20
DEFAULTxlabel_font = 15
DEFAULTylabel_font = 15
DEFAULTytick_font = 8
DEFAULTanno_font = 10


def setUnitData(unit_data, wannasave):
    if unit_data:
        if 'HIGHESTY' in unit_data.sections():
            highest_unit = unit_data['HIGHESTY']
        else:
            highest_unit = HIGHESTY
        if wannasave and 'SAVE FONT' in unit_data.sections():
            title_font = unit_data['SAVE FONT']['Title Font']
            xlabel_font = unit_data['SAVE FONT']['Xlabel Font']
            ylabel_font = unit_data['SAVE FONT']['Ylabel Font']
            ytick_font = unit_data['SAVE FONT']['Ytick Font']
            anno_font = unit_data['SAVE FONT']['Anno Font']
        elif 'SCREEN FONT' in unit_data.sections():
            title_font = unit_data['SCREEN FONT']['Title Font']
            xlabel_font = unit_data['SCREEN FONT']['Xlabel Font']
            ylabel_font = unit_data['SCREEN FONT']['Ylabel Font']
            ytick_font = unit_data['SCREEN FONT']['Ytick Font']
            anno_font = unit_data['SCREEN FONT']['Anno Font']
        else:
            title_font = DEFAULTtitle_font
            xlabel_font = DEFAULTxlabel_font
            ylabel_font = DEFAULTylabel_font
            ytick_font = DEFAULTytick_font
            anno_font = DEFAULTanno_font
        if 'BAR COLOR' in unit_data.sections():
            bar_color = unit_data['BAR COLOR']
        else:
            bar_color = DEFAULTBARCOLOR
        if 'LINE COLOR'in unit_data.sections():
            line_color = unit_data['LINE COLOR']
        else:
            line_color = DEFAULTLINECOLOR
        if 'GRAPH OPTION' in unit_data.sections():
            marker = unit_data['GRAPH OPTION']['marker']
            line_style = unit_data['GRAPH OPTION']['line style']
            scatter_size = int(unit_data['GRAPH OPTION']['scatter size'])
            bar_alpha = float(unit_data['GRAPH OPTION']['bar alpha'])
        else:
            marker = DEFAULTMARKER
            line_style = DEFAULTLINESTYLE
            scatter_size = DEFAULTSCATTERSIZE
            bar_alpha = DEFAULTBARALPHA
    else:
        highest_unit = HIGHESTY
        title_font = DEFAULTtitle_font
        xlabel_font = DEFAULTxlabel_font
        ylabel_font = DEFAULTylabel_font
        ytick_font = DEFAULTytick_font
        anno_font = DEFAULTanno_font
        bar_color = DEFAULTBARCOLOR
        line_color = DEFAULTLINECOLOR
        marker = DEFAULTMARKER
        line_style = DEFAULTLINESTYLE
        scatter_size = DEFAULTSCATTERSIZE
        bar_alpha = DEFAULTBARALPHA

    return highest_unit, title_font, xlabel_font, ylabel_font, ytick_font, anno_font, bar_color, line_color, marker, line_style, scatter_size, bar_alpha


def plotBar(ax, day_type, bar_type, bar_data, xlabel, wannasave, val, title, unit_data, temp_data=None):
    highest_unit, title_font, xlabel_font, ylabel_font, ytick_font, anno_font, bar_color, line_color, marker, line_style, scatter_size, bar_alpha = setUnitData(
        unit_data, wannasave)

    try:
        xaxis = np.arange(len(xlabel))
        bar_num = len(bar_data)
        width = 0.5 - 0.1*(bar_num-1)
        higest_bar_unit = []
        lowest_bar_unit = []
        bottom_base = 0

        for i, (key, value) in enumerate(bar_data.items()):
            if bar_type[1] == 'group' and bar_type[2] in WEIGHT_ANNOTATION:
                ax.bar(xaxis+(i-(bar_num-1)/2)*width, value, color=(value > 0).map({True: 'r', False: 'g'}), align='center',
                       width=width, alpha=bar_alpha, label=key)
                ax.axhline(y=0, c='k', alpha=0.5, ls='--', lw=0.3)
                point_val = list(temp_data.values())[i]
                point_val = point_val.values
                for k, p in enumerate(ax.patches):
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate("%.1f" %
                                (point_val[k]), (left+width/2, height/2), ha='center', fontsize=anno_font)
            elif bar_type[1] == 'group':
                if bar_type[2] in MONOSTRAIN_ANNOTATION:
                    ax.bar(xaxis+(i-(bar_num-1)/2)*width, value, color=(value < 6000).map({True: bar_color[str(i)], False: 'r'}), align='center',
                           width=width, alpha=bar_alpha, label=key)
                elif bar_type[2] in FIVELEVEL_ANNOTATION:
                    color_dict = {1: bar_color['2'], 2: bar_color['2'],
                                  3: bar_color['0'], 4: bar_color['1'], 5: bar_color['1']}
                    ax.bar(xaxis+(i-(bar_num-1)/2)*width, value, color=color_dict[value], align='center',
                           width=width, alpha=bar_alpha, label=key)
                else:
                    ax.bar(xaxis+(i-(bar_num-1)/2)*width, value, color=bar_color[str(i)], align='center',
                           width=width, alpha=bar_alpha, label=key)
                if bar_type[2] in ['DG_Player MSR', 'DG_Player HSR', 'DG_Player Sprint']:
                    ax.axhline(y=value.describe()[
                        'mean'], c='r', alpha=1, ls='--', lw=1, label="{} average".format(key))
                if val and bar_type[2] in BAR_ANNOTATION:
                    for p in ax.patches:
                        left, bottom, width, height = p.get_bbox().bounds
                        ax.annotate("%.1f" %
                                    (height), (left+width/2, height/2), ha='center', fontsize=anno_font)
            elif bar_type[1] == 'stack':
                ax.bar(xaxis, value, bottom=bottom_base,
                       color=bar_color[str(i)], alpha=bar_alpha, label=key)
                bottom_base += value
                if val and bar_type[2] in BAR_ANNOTATION:
                    for p in ax.patches:
                        left, bottom, width, height = p.get_bbox().bounds
                        ax.annotate("%.2f" % (height), (left+width /
                                                        2, bottom+height/2), ha='center', fontsize=anno_font)
            else:
                return None

            higest_bar_unit.append(
                int(highest_unit.get(key.split(':')[0], 1000)))
            lowest_bar_unit.append(LOWESTY.get(key.split(':')[0], 0))
            if i == 0:
                axlabel = GRAPHUNIT.get(key.split(':')[0], 'Distance(m)')
                x_num = len(value)
                if x_num < 10:
                    rotation = 0
                elif x_num < 30:
                    rotation = -30
                else:
                    rotation = -90

        ax.legend(loc=2)
        ax.set_xticks(xaxis)
        ax.set_xticklabels(
            list(xlabel), rotation=rotation, ha='left', fontsize=xlabel_font)
        ax.set_ylabel(axlabel, fontsize=ylabel_font)
        ax.set_ylim([np.array(lowest_bar_unit).min(),
                     np.array(higest_bar_unit).max()])
        ax.tick_params(axis="y", labelsize=ytick_font)
        ax.grid(b=True, which='major', axis='x')
        ax.set_title("{} : {}".format(
            title, bar_type[2].split('_')[1]), fontsize=title_font, pad=10.)
    except:
        pass


def plotLine(ax, day_type, line_type, line_data, xlabel, wannasave, val, title, unit_data, temp_data=None):
    highest_unit, title_font, xlabel_font, ylabel_font, ytick_font, anno_font, bar_color, line_color, marker, line_style, scatter_size, bar_alpha = setUnitData(
        unit_data, wannasave)

    if line_data:
        xaxis = np.arange(len(xlabel))
        line_num = len(line_data)
        higest_line_unit = []
        lowest_line_unit = []

        for j, (key, value) in enumerate(line_data.items()):
            if line_type[2] in ['DG_Player Distance', 'PG_Distance']:
                if day_type == 'M':
                    ax.axhline(y=value.sum()/10, c='r', alpha=1, ls='--',
                               lw=1, label="{} average".format(key))
                else:
                    ax.axhline(y=value.describe()[
                        'mean'], c='r', alpha=1, ls='--', lw=1, label="{} average".format(key))

            if line_type[1] == 'scatter':
                ax.scatter(xaxis, value, c=line_color[str(j)], marker='o',
                           label=key, s=scatter_size)
            elif line_type[1] == 'line':
                ax.plot(
                    xaxis, value, c=line_color[str(j)], marker=marker, ls=line_style, label=key)
            else:
                return None

            if val and line_type[2] in LINE_ANNOTATION:
                for value, xcount, ycount in zip(value, xaxis, value):
                    ax.annotate("%.1f" % value, xy=(
                        xcount, ycount), xytext=(-7, 10), textcoords='offset points', color=line_color[str(j)][0], fontsize=anno_font)
            higest_line_unit.append(
                int(highest_unit.get(key.split(':')[0], 1000)))
            lowest_line_unit.append(LOWESTY.get(key.split(':')[0], 0))
            if j == 0:
                axtlabel = GRAPHUNIT.get(key.split(':')[0], 'Distance(m)')

        ax.legend(loc=1)
        ax.set_ylabel(axtlabel, fontsize=ylabel_font)
        ax.set_ylim([np.array(lowest_line_unit).min(),
                     np.array(higest_line_unit).max()])
        ax.tick_params(axis="y", labelsize=ytick_font)
        ax.set_title("{} : {}".format(
            title, line_type[2].split('_')[1]), fontsize=title_font, pad=10.)
    else:
        pass


"""
'b' blue / 'g' green / 'r' red / 'c' cyan / 'm' magenta / 'y' yellow / 'k' black / 'w' white

'.' point / ',' pixel / 'o' circle / 'v' triangle_down / '^' triangle_up / '<' tri_left / '>' tri_right / 's' squre / 'p' pentagon
'*' star / 'h''H' hexagon / '+' plus / 'x' x / 'd''D' diamond / '|' vline / '_' hline
'-' solid line / '--' dashed lind / '-.' dase-dot line / ':' dotted line
"""

"""
[Player Graph]
Distance : Line(Total_dist) mean HL(red), annotation Bar only
Load : Line(GPS_PL) mean HL(red)
Mono & Strain : Bar(strain) > 6,000 DEFAULTBARCOLOR(Red), if possible Line(mono) < 1.1 / < 1.8 / else
MSR, HSR, Sprint : 
Weight : 
Body Index :

[Day Graph] 
Position Distance : Scatter(Total_dist) mean HL(red), annotation Bar & Line
Player Distance : Scatter(Total_dist) mean HL(red), annotation Bar only
Player Mono & Strain : Bar(strain) > 6,000 DEFAULTBARCOLOR(Red), if possible Scatter(mono) < 1.1 / < 1.8 / else
Player Weight : 

{Bar annotation}
'PG_Distance', 'PG_Load','PG_Mono & Starin', 'PG_MSR', 'PG_HSR', 'PG_Sprint', 'PG_Body Index', 'DG_Position Distance','DG_Player Distance','DG_Player Mono & Starin'
{Line annotation}
'PG_Load','PG_Body Index','DG_Position Distance'
{Bar color}
>6000 'PG_Mono & Strain', 'DG_Player Mono & Strain'
>0 'DG_Player Weight'
{Line mean HL}
'PG_Distance', 'PG_Laod', 'DG_Position Distance','DG_Player Distance' 
"""
