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
    'Position Distance': '#001_Day Position Distance',
    'Player Distance': '#002_Day Player Distance',
    'Day Mono, Strain': '#003_Day Mono, Strain',
    'Player Accel, Decel': '#004_Day Accel, Decel',
    'Day Weight Change': '#005_Day Wellness',
    'Day Body Index': '#005_Day Wellness',
    'Distance': '#006_Player Distance',
    'Load': '#007_Player Load',
    'Mono, Strain': '#008_Player Mono, Strain',
    'MSR': '#009_Player MSR',
    'HSR': '#010_Player HSR',
    'Sprint': '#011_Player Sprint',
    'Sleep': '#012_Player Wellness',
    'Body Index': '#012_Player Wellness',
    'Total': '#013_Total'
}

DB_CONFIG = {
    'session': 'session_db.pickle',
    'wellness': 'wellness_db.pickle',
    'dayInfo': 'dayInfo_db.pickle',
    'player': 'player_db.pickle',
    'match': 'match_db.pickle'
}
