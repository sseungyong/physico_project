import os
import sys

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
    'Dist. Load': 'Load',
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
    'TR Time <SUM>': 500,
    'Total Dist. <SUM>': 50000,
    'Dist. per min <SUM>': 1000,
    'MSR <SUM>': 8000,
    'HSR <SUM>': 4000,
    'Sprint <SUM>': 1000,
    'Accel Cnt. <SUM>': 100,
    'Decel Cnt. <SUM>': 100
}

LOWESTY = {
    'Weight Change': -3
}
