import os

ROOT_CONFIG = {
    'base': os.path.dirname(os.getcwd())
}

FOLDER_CONFIG = {
    'input': '#01_input_data',
    'output': '#02_result_data',
    'graph': '#03_graph_data',
    'backup': '_back_up_dont_touch'
}

FILE_CONFIG = {
    'day': 'result_by_day.xlsx',
    'player': 'result_by_player.xlsx',
    'match': 'result_by_match.xlsx'
}

DATA_CONFIG = {
    'file': 'file_data.pickle',
    'session': 'session_data.pickle',
    'day': 'day_data.pickle',
    'player': 'player_data.pickle',
    'match': 'match_data.pickle',
}

INPUT_CONFIG = {
    'workout': '#001_workout',
    'wellness': '#002_wellness'
}

RESULT_CONFIG = {
    'day': '#001_Day',
    'player': '#002_Player',
    'match': '#003_Match'
}

IMAGE_CONFIG = {
    'Day Graph': '#001_Day Graph',
    'Match Day Graph': '#002_Match Day Graph',
    'Match Period Graph': '#003_Match Period Graph',
    'Player Graph': '#004_Player Graph',
}

IMAGE_DAY_CONFIG = {
    'Position Distance': '#0001_Day Position Distance',
    'Player Distance': '#0002_Day Player Distance',
    'Player MSR': '#0002_Day Player Distance',
    'Player HSR': '#0002_Day Player Distance',
    'Player Sprint': '#0002_Day Player Distance',
    'Player Accel, Decel': '#0003_Day Accel, Decel',
    'Day Mono, Strain': '#0004_Day Mono, Strain',
    'Day Weight Change': '#0005_Day Wellness',
    'Day Sleep': '#0005_Day Wellness',
    'Day Muscle': '#0005_Day Wellness',
    'Day Body Index': '#0005_Day Wellness',
    'Total': '#0006_Total'
}

IMAGE_MATCHDAY_CONFIG = {
    'Team Time Distance': '#0001_Team Distance',
    'Position Average Distance': '#0002_Position Distance',
    'Position Sum Distance': '#0002_Position Distance',
    'Player Distance': '#0003_Player Distance',
    'Player Total Time & Dist.': '#0004_Player Time & Dist.',
    'Player Total Time & HSR': '#0005_Player Time & HSR',
    'Player Total Time & Sprint': '#0006_Player Time & Sprint',
    'Player Total Time & Dist. per min': '#0007_Player Time & Dist. per min',
    'Player Accel, Decel': '#0008_Player Accel, Decel',
    'Total': '#0009_Total'
}

IMAGE_MATCHPERIOD_CONFIG = {
    'Period Team Distance': '#0001_Team Distance',
    'Period Team Accel, Decel': '#0002_Team Accel, Decel',
    'Period Team Load': '#0003_Team Load',
    'Period Team Dist. Load': '#0003_Team Load',
    # On / Off
    'Period OnOff Distance': '#0001_Team Distance',
    'Period OnOff Accel, Decel': '#0002_Team Accel, Decel',
    'Period OnOff Load': '#0003_Team Load',
    'Period OnOff Dist. Load': '#0003_Team Load',
    'Total': '#0004_Total'
}

IMAGE_PLAYER_CONFIG = {
    'Distance': '#0001_Player Distance',
    'Load': '#0002_Player Load',
    'Dist. Load': '#0002_Player Load',
    'MSR': '#0003_Player MSR',
    'HSR': '#0004_Player HSR',
    'Sprint': '#0005_Player Sprint',
    'Accel, Decel': '#0006_Player Accel, Decel',
    'Max Speed': '#0007_Player Max Speed',
    'Mono, Strain': '#0008_Player Mono, Strain',
    'Weight Change': '#0009_Player Wellness',
    'Sleep': '#0009_Player Wellness',
    'Muscle': '#0009_Player Wellness',
    'Body Index': '#0009_Player Wellness',
    'Total': '#0010_Total'
}

DB_CONFIG = {
    'session': 'session_db.pickle',
    'wellness': 'wellness_db.pickle',
    'dayInfo': 'dayInfo_db.pickle',
    'player': 'player_db.pickle',
    'match': 'match_db.pickle'
}
