import os
import sys

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
    'Player MSR': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player MSR'),
            'needData': [('Player', 'MSR')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player MSR'),
            'needData': [('Player', 'Total Dist.')]
        }
    },
    'Player HSR': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player HSR'),
            'needData': [('Player', 'HSR')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player HSR'),
            'needData': [('Player', 'Total Dist.')]
        }
    },
    'Player Sprint': {
        'Bar': {
            'wannaType': ('Player', 'group', 'DG_Player Sprint'),
            'needData': [('Player', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'DG_Player Sprint'),
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
    'Team Time Distance': {
        'Bar': {
            'wannaType': ('Position', 'group', 'MG_Team Time Distance'),
            'needData': [('Position', 'MSR'), ('Position', 'HSR'), ('Position', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Position', 'scatter', 'MG_Team Time Distance'),
            'needData': [('Position', 'Total Dist.')]
        }
    },
    'Position Average Distance': {
        'Bar': {
            'wannaType': ('Position Average', 'group', 'MG_Position Average Distance'),
            'needData': [('Position Average', 'MSR'), ('Position Average', 'HSR'), ('Position Average', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Position Average', 'scatter', 'MG_Position Average Distance'),
            'needData': [('Position Average', 'Total Dist.')]
        }
    },
    'Position Sum Distance': {
        'Bar': {
            'wannaType': ('Position Sum', 'group', 'MG_Position Sum Distance'),
            'needData': [('Position Sum', 'MSR <SUM>'), ('Position Sum', 'HSR <SUM>'), ('Position Sum', 'Sprint <SUM>')]
        },
        'Line': {
            'wannaType': ('Position Sum', 'scatter', 'MG_Position Sum Distance'),
            'needData': [('Position Sum', 'Total Dist. <SUM>')]
        }
    },
    'Player Distance': {
        'Bar': {
            'wannaType': ('Player', 'group', 'MG_Player Distance'),
            'needData': [('Player', 'MSR'), ('Player', 'HSR'), ('Player', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'MG_Player Distance'),
            'needData': [('Player', 'Total Dist.')]
        }
    },
    'Player Total Time & Dist.': {
        'Bar': {
            'wannaType': ('Player', 'group', 'MG_Player Total Time & Dist.'),
            'needData': [('Player', 'TR Time')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'MG_Player Total Time & Dist.'),
            'needData': [('Player', 'Total Dist.')]
        }
    },
    'Player Total Time & HSR': {
        'Bar': {
            'wannaType': ('Player', 'group', 'MG_Player Total Time & HSR'),
            'needData': [('Player', 'TR Time')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'MG_Player Total Time & HSR'),
            'needData': [('Player', 'HSR')]
        }
    },
    'Player Total Time & Sprint': {
        'Bar': {
            'wannaType': ('Player', 'group', 'MG_Player Total Time & Sprint'),
            'needData': [('Player', 'TR Time')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'MG_Player Total Time & Sprint'),
            'needData': [('Player', 'Sprint')]
        }
    },
    'Player Total Time & Dist. per min': {
        'Bar': {
            'wannaType': ('Player', 'group', 'MG_Player Total Time & Dist. per min'),
            'needData': [('Player', 'TR Time')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'MG_Player Total Time & Dist. per min'),
            'needData': [('Player', 'Dist. per min')]
        }
    },
    'Player Accel, Decel': {
        'Bar': {
            'wannaType': ('Player', 'group', 'MG_Player Accel, Decel'),
            'needData': [('Player', 'Accel Cnt.'), ('Player', 'Decel Cnt.')]
        },
        'Line': {
            'wannaType': ('Player', 'scatter', 'MG_Player Accel, Decel'),
            'needData': []
        }
    },
}

MATCHPERIODGRAPHTYPE = {
    'Period Team Distance': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PM_Player Distance'),
            'needData': [('Player', 'MSR'), ('Player', 'HSR'), ('Player', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PM_Player Distance'),
            'needData': [('Player', 'Total Dist.')]
        }
    },
    'Period Team Accel, Decel': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PM_Player Accel, Decel'),
            'needData': [('Player', 'Accel Cnt.'), ('Player', 'Decel Cnt.')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PM_Player Accel, Decel'),
            'needData': []
        }
    },
    'Period Team Load': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PM_Player Load'),
            'needData': [('Player', 'Total Dist.')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PM_Player Load'),
            'needData': [('Player', 'GPS PL'), ('Player', 'Load')]
        }
    },
    'Period Team Dist. Load': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PM_Player Load'),
            'needData': [('Player', 'Total Dist.')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PM_Player Load'),
            'needData': [('Player', 'Dist. Load'), ('Player', 'Load')]
        }
    },
    # On / Off
    'Period OnOff Distance': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PM_Player Distance'),
            'needData': [('Player', 'MSR'), ('Player', 'HSR'), ('Player', 'Sprint')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PM_Player Distance'),
            'needData': [('Player', 'Total Dist.:On'), ('Player', 'Total Dist.:Off')]
        }
    },
    'Period OnOff Accel, Decel': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PM_Player Accel, Decel'),
            'needData': [('Player', 'Accel Cnt.:On'), ('Player', 'Accel Cnt.:Off')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PM_Player Accel, Decel'),
            'needData': [('Player', 'Decel Cnt.:On'), ('Player', 'Decel Cnt.:Off')]
        }
    },
    'Period OnOff Load': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PM_Player Load'),
            'needData': [('Player', 'GPS PL:On'), ('Player', 'GPS PL:Off')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PM_Player Load'),
            'needData': [('Player', 'Load:On'), ('Player', 'Load:Off')]
        }
    },
    'Period OnOff Dist. Load': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PM_Player Load'),
            'needData': [('Player', 'Dist. Load:On'), ('Player', 'Dist. Load:Off')]
        },
        'Line': {
            'wannaType': ('Player', 'line', 'PM_Player Load'),
            'needData': [('Player', 'Load:On'), ('Player', 'Load:Off')]
        }
    },
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
    'Dist. Load': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Load'),
            'needData':  [('Team', 'Total Dist.'), ('Player', 'Total Dist.')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_Load'),
            'needData':  [('Player', 'Dist. Load'), ('Player', 'Load')]
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
    'Accel, Decel': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Accel, Decel'),
            'needData':  [('Player', 'Accel Cnt.'), ('Player', 'Decel Cnt.')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_Max Speed'),
            'needData':  []
        }
    },
    'Max Speed': {
        'Bar': {
            'wannaType': ('Date', 'group', 'PG_Accel, Decel'),
            'needData':  [('Player', 'Max Speed')]
        },
        'Line': {
            'wannaType': ('Date', 'line', 'PG_Max Speed'),
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
