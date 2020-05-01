import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
font_set = [(f.name, f.fname)
            for f in fm.fontManager.ttflist if ('Nanum' in f.name) | ('HY' in f.name) | ('Apple' in f.name)]
font = font_set[3]
font_name = font[0]
matplotlib.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

LINECOLOR = {0: 'ks--', 1: 'gs--', 2: 'ms--', 3: 'rs--'}
DEFAULTBARCOLOR = {0: 'y', 1: 'b', 2: 'r', 3: 'k'}
GRAPHUNIT = {
    'Height': 'Height(cm)',
    'Weight': 'Weight(kg)',
    'RPE_1': 'RPE',
    'RPE_2': 'RPE',
    'RPE_3': 'RPE',
    'TR Time': 'Time(min)',
    'Accel Cnt.': 'Count',
    'Decel Cnt.': 'Count',
    'Max Speed': 'Speed(km/h)',
    'GPS PL': 'Load',
    'Load': 'Load',
    'Mono': 'Mono',
    'Strain': 'Strain',
    'EWAM': 'EWAM',
    'Sleep': 'Point',
    'Muscle': 'Point',
    'Sleep Time': 'Hours',
    'Body Muscle': 'Weight(kg)',
    'Body Fat': 'Percent(%)',
    'Weight Change': 'Percent(%)',
    'MSR %': 'Percent(%)',
    'HSR %': 'Percent(%)',
    'Sprint %': 'Percent(%)'
}

HIGHESTY = {
    'Height': 200,
    'Weight': 100,
    'RPE': 12,
    'RPE_1': 12,
    'RPE_2': 12,
    'RPE_3': 12,
    'TR Time': 200,
    'Total Dist.': 15000,
    'MSR': 6000,
    'HSR': 2500,
    'Sprint': 1000,
    'Accel Cnt.': 30,
    'Decel Cnt.': 30,
    'Max Speed': 30,
    'GPS PL': 1000,
    'Load': 1000,
    'Mono': 6,
    'Strain': 15000,
    'EWAM': 1.2,
    'Sleep': 6,
    'Muscle': 6,
    'Sleep Time': 10,
    'Body Muscle': 50,
    'Body Fat': 30,
    'Weight Change': 3,
    'MSR %': 50,
    'HSR %': 50,
    'Sprint %': 50,
}

LOWESTY = {
    'Weight Change': -3
}

PLAYERGRAPHTYPE = {
    'Distance': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Distance'),
            'needData':  [('Player', 'Dist. per min'), ('Player', 'Sprint'), ('Player', 'HSR')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_Distance'),
            'needData':  [('Player', 'Total Dist.')]
        }
    },
    'Load': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Load'),
            'needData':  [('Team', 'Total Dist.'), ('Player', 'Total Dist.')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_Load'),
            'needData':  [('Player', 'GPS PL'), ('Player', 'Load')]
        }
    },
    'Mono, Strain': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Mono & Strain'),
            'needData':  [('Player', 'Strain')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_Mono & Strain'),
            'needData':  [('Player', 'Mono')]
        }
    },
    'MSR': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_MSR'),
            'needData':  [('Team', 'MSR'), ('Player', 'MSR')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_MSR'),
            'needData':  []
        }
    },
    'HSR': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_HSR'),
            'needData':  [('Team', 'HSR'), ('Player', 'HSR')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_HSR'),
            'needData':  []
        }
    },
    'Sprint': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Sprint'),
            'needData':  [('Team', 'Sprint'), ('Player', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_Sprint'),
            'needData':  []
        }
    },
    'Sleep': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Sleep'),
            'needData':  [('Player', 'Sleep'), ('Player', 'Muscle')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_Sleep'),
            'needData':  [('Player', 'Sleep Time')]
        }
    },
    'Body Index': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Body Index'),
            'needData':  [('Player', 'Weight'), ('Player', 'Body Muscle')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_Body Index'),
            'needData':  [('Player', 'Body Fat')]
        }
    },
    'Weight Change': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Player Weight'),
            'needData': [('Player', 'Weight Change')]
        },
        'Line': {
            'wannaType': ('Date', 'nan', 'PG_Player Weight'),
            'needData': [('Player', 'Weight')]
        }
    }
}

DAYGRAPHTYPE = {
    'Position Distance': {
        'Bar': {
            'wannaType': ('Position', 'group', 'DG_Position Distance'),
            'needData': [('Position', 'MSR'), ('Position', 'HSR'), ('Position', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Position', 'scatter', 'DG_Position Distance'),
            'needData': [('Position', 'Total Dist.')]
        }
    },
    'Player Distance': {
        'Bar': {
            'wannaType': ('Player', 'stack', 'DG_Player Distance'),
            'needData': [('Player', 'MSR %'), ('Player', 'HSR %'), ('Player', 'Sprint %')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player Distance'),
            'needData': [('Player', 'Total Dist.')]
        }
    },
    'Day Mono, Strain': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player Mono & Strain'),
            'needData': [('Player', 'Strain')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player Mono & Strain'),
            'needData': [('Player', 'Mono')]
        }
    },
    'Player Accel, Decel': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player Accel, Decel'),
            'needData': [('Player', 'Accel Cnt.'), ('Player', 'Decel Cnt.')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player Accel, Decel'),
            'needData': []
        }
    },
    'Day Weight Change': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player Weight'),
            'needData': [('Player', 'Weight Change')]
        },
        'Line': {
            'wannaType': ('Player', 'nan', 'DG_Player Weight'),
            'needData': [('Player', 'Weight')]
        }
    },
    'Day Body Index': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Body Index'),
            'needData':  [('Player', 'Weight'), ('Player', 'Body Muscle')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'DG_Body Index'),
            'needData':  [('Player', 'Body Fat')]
        }
    }
}

MATCHGRAPHTYPE = {
    'Position Distance': {
        'Bar': {
            'wannaType': ('Position', 'group', 'DG_Position Distance'),
            'needData': [('Position', 'MSR'), ('Position', 'HSR'), ('Position', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Position', 'scatter', 'DG_Position Distance'),
            'needData': [('Position', 'Total Dist.')]
        }
    },
    'Player Distance': {
        'Bar': {
            'wannaType': ('Player', 'stack', 'DG_Player Distance'),
            'needData': [('Player', 'MSR %'), ('Player', 'HSR %'), ('Player', 'Sprint %')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player Distance'),
            'needData': [('Player', 'Total Dist.')]
        }
    },
    'Player Total Time & Dist.': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player Total Time & Dist.'),
            'needData': [('Player', 'TR Time')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player Total Time & Dist.'),
            'needData': [('Player', 'Total Dist.')]
        }
    },
    'Player Total Time & HSR': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player Total Time & HSR'),
            'needData': [('Player', 'TR Time')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player Total Time & HSR'),
            'needData': [('Player', 'HSR')]
        }
    },
    'Player Total Time & Sprint': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player Total Time & Sprint'),
            'needData': [('Player', 'TR Time')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player Total Time & Sprint'),
            'needData': [('Player', 'Sprint')]
        }
    },
    'Player Accel, Decel': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player Accel, Decel'),
            'needData': [('Player', 'Accel Cnt.'), ('Player', 'Decel Cnt.')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player Accel, Decel'),
            'needData': []
        }
    }
}

MATCHPERIODGRAPHTYPE = {
    'Period Distance': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Player Distance'),
            'needData': [('Player', 'MSR'), ('Player', 'HSR'), ('Player', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PG_Player Distance'),
            'needData': [('Player', 'Total Dist.'), ('Player', 'Team_Total Dist.')]
        }
    },
    'Period Accel, Decel': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Player Accel, Decel'),
            'needData': [('Player', 'Accel Cnt.'), ('Player', 'Decel Cnt.')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PG_Player Accel, Decel'),
            'needData': [('Player', 'Team_Accel Cnt.'), ('Player', 'Team_Decel Cnt.')]
        }
    },
    'Period Load': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Player Load'),
            'needData': [('Player', 'Total Dist.')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PG_Player Load'),
            'needData': [('Player', 'GPS PL'), ('Player', 'Load'), ('Player', 'Team_Load')]
        }
    },
}

TRPOSITIONLIST = ['CB', 'SB', 'FB', 'CMF',
                  'DMF', 'AMF', 'MF', 'WF', 'FW', 'Team']
MPOSITIONLIST = ['1st Half Avg.',
                 '2nd Half Avg.', 'Total Avg.', 'Reserve Avg.']

# Parameters

DEFAULTtitle_font = 20
DEFAULTxlabel_font = 15
DEFAULTylabel_font = 15
DEFAULTytick_font = 8
DEFAULTanno_font = 10


def plotBar(ax, day_type, bar_type, bar_data, xlabel, wannasave, val, title, unit_data, temp_data=None):
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
    else:
        highest_unit = HIGHESTY
        title_font = DEFAULTtitle_font
        xlabel_font = DEFAULTxlabel_font
        ylabel_font = DEFAULTylabel_font
        ytick_font = DEFAULTytick_font
        anno_font = DEFAULTanno_font

    try:
        xaxis = np.arange(len(xlabel))
        bar_num = len(bar_data)
        width = 0.5 - 0.1*(bar_num-1)
        higest_bar_unit = []
        lowest_bar_unit = []
        bottom_base = 0

        for i, (key, value) in enumerate(bar_data.items()):
            if bar_type[1] == 'group' and bar_type[2] in ['PG_Player Weight', 'DG_Player Weight']:
                ax.bar(xaxis+(i-(bar_num-1)/2)*width, value, color=(value > 0).map({True: 'r', False: 'g'}), align='center',
                       width=width, alpha=0.4, label=key)
                ax.axhline(y=0, c='k', alpha=0.5, ls='--', lw=0.3)
                point_val = list(temp_data.values())[i]
                point_val = point_val.values
                for k, p in enumerate(ax.patches):
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate("%.1f" %
                                (point_val[k]), (left+width/2, height/2), ha='center', fontsize=anno_font)
            elif bar_type[1] == 'group':
                if bar_type[2] in ['PG_Mono & Strain', 'DG_Player Mono & Strain']:
                    ax.bar(xaxis+(i-(bar_num-1)/2)*width, value, color=(value < 6000).map({True: DEFAULTBARCOLOR[i], False: 'r'}), align='center',
                           width=width, alpha=0.4, label=key)
                else:
                    ax.bar(xaxis+(i-(bar_num-1)/2)*width, value, color=DEFAULTBARCOLOR[i], align='center',
                           width=width, alpha=0.4, label=key)
                if val and bar_type[2] in ['PG_Distance', 'PG_Load', 'PG_Mono & Strain', 'PG_MSR', 'PG_HSR', 'PG_Sprint', 'PG_Body Index', 'DG_Position Distance', 'DG_Player Distance', 'DG_Player Mono & Strain', 'DG_Player Accel, Decel', 'DG_Player Total Time & Dist.', 'DG_Player Total Time & HSR', 'DG_Player Total Time & Sprint']:
                    for p in ax.patches:
                        left, bottom, width, height = p.get_bbox().bounds
                        ax.annotate("%.1f" %
                                    (height), (left+width/2, height/2), ha='center', fontsize=anno_font)
            elif bar_type[1] == 'stack':
                ax.bar(xaxis, value, bottom=bottom_base,
                       color=DEFAULTBARCOLOR[i], alpha=0.4, label=key)
                bottom_base += value
                if val and bar_type[2] in ['PG_Distance', 'PG_Load', 'PG_Mono & Strain', 'PG_MSR', 'PG_HSR', 'PG_Sprint', 'PG_Body Index', 'DG_Position Distance', 'DG_Player Distance', 'DG_Player Mono & Strain', 'DG_Player Accel, Decel', 'DG_Player Total Time & Dist.', 'DG_Player Total Time & HSR', 'DG_Player Total Time & Sprint']:
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
    else:
        highest_unit = HIGHESTY
        title_font = DEFAULTtitle_font
        xlabel_font = DEFAULTxlabel_font
        ylabel_font = DEFAULTylabel_font
        ytick_font = DEFAULTytick_font
        anno_font = DEFAULTanno_font

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
                ax.scatter(xaxis, value, c='k', marker='o', label=key, s=50)
            elif line_type[1] == 'line':
                ax.plot(xaxis, value, LINECOLOR[j], label=key)
            else:
                return None

            if val and line_type[2] in ['PG_Load', 'PG_Body Index', 'DG_Position Distance', 'DG_Player Total Time & Dist.', 'DG_Player Total Time & HSR', 'DG_Player Total Time & Sprint']:
                for value, xcount, ycount in zip(value, xaxis, value):
                    ax.annotate("%.1f" % value, xy=(
                        xcount, ycount), xytext=(-7, 10), textcoords='offset points', color=LINECOLOR[j][0], fontsize=anno_font)
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
