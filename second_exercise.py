import numpy as np
import pathlib
import matplotlib.pyplot as plt
import data_utils
import re
import math
from enum import Enum

# Data related
DATA_PATH = pathlib.Path("./data")
AVERAGE_TEMPERATURE_FILE = DATA_PATH.joinpath("gaisaTemperatura2022.xlsx")
CHART_TITLE = "Gaisa temperatūra Rīgā četros gadalaikos"
# X_LABEL = ""
Y_LABEL = "Gaisa temperatūra (Celsija grādi)"
X_LABEL_INDEX = 0
Y_LABEL_INDEX = 0
SEASON_COUNT = 4
SEASONS = Enum('Color', ["Ziema", "Pavasaris", "Vasara", "Rudens"], start=0)
MONTHS_TO_SEASONS = {
    # Ziema
    1: SEASONS(0).value,
    2: SEASONS(0).value,
    # Pavasaris
    3: SEASONS(1).value,
    4: SEASONS(1).value,
    5: SEASONS(1).value,
    # Vasara
    6: SEASONS(2).value,
    7: SEASONS(2).value,
    8: SEASONS(2).value,
    # Rudens
    9: SEASONS(3).value,
    10: SEASONS(3).value,
    11: SEASONS(3).value,
    12: SEASONS(0).value,
}

# Matplotlib configuration
CHART_FILENAME = "second_exercise.png"
CHART_SAVE_PATH = pathlib.Path(CHART_FILENAME)
# BAR_WIDTH = 0.8
PX = 1 / plt.rcParams['figure.dpi']
FIG_SIZE = (1200 * PX, 1200 * PX)

spreadsheet = data_utils.get_work_sheet_by_index(AVERAGE_TEMPERATURE_FILE,
                                                 index=0)
data_arr = data_utils.array_from_sheet(spreadsheet, X_LABEL_INDEX,
                                       Y_LABEL_INDEX)
y_labels = data_utils.get_y_labels(spreadsheet, X_LABEL_INDEX, Y_LABEL_INDEX)
season_day_count = {item.name: 0 for item in SEASONS}
total_day_count = len(y_labels)

for label in y_labels:
    month_num_str = re.match(r'\d+\.(\d+)\.\d+', label).group(1)
    month_num_str = re.sub(r'^0+', '', month_num_str)
    month_num = int(month_num_str)
    season_num = MONTHS_TO_SEASONS[month_num]
    season_name = SEASONS(season_num).name
    season_day_count[season_name] += 1

season_starting_indexes = {
    item[0]: sum(list(season_day_count.values())[0:i])
    for i, item in enumerate(season_day_count.items())
}

# Initalize the array

maximal_length_of_season = max(season_day_count.values())
season_data = np.array([
    np.full(maximal_length_of_season, np.nan) for i in range(0, len(SEASONS))
])


def get_index_of_first_less_or_equal(n, list_):
    index_ = -1
    for item in enumerate(list_):
        i, val = item
        if n >= val:
            index_ = i
    return index_


for i, row in enumerate(data_arr):
    day_average = np.average(row)
    index_ = get_index_of_first_less_or_equal(
        i, list(season_starting_indexes.values()))
    # TODO: complete collection of day averages
