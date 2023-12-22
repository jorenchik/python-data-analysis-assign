import numpy as np
import pathlib
import matplotlib.pyplot as plt
import data_utils
import re
from enum import Enum

# Data related
DATA_PATH = pathlib.Path("./data")
AVERAGE_TEMPERATURE_FILE = DATA_PATH.joinpath("gaisaTemperatura2022.xlsx")
CHART_TITLE = "Gaisa temperatūra Rīgā četros gadalaikos"
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
MAXIMUM_DAYS_IN_A_MONTH = 31
MONTHS_PER_SEASON = 3


def get_index_of_first_less_or_equal(n, list_):
    index_ = -1
    for item in enumerate(list_):
        i, val = item
        if n >= val:
            index_ = i
    return index_


spreadsheet = data_utils.get_work_sheet_by_index(AVERAGE_TEMPERATURE_FILE,
                                                 index=0)
data_arr = data_utils.array_from_sheet(spreadsheet, X_LABEL_INDEX,
                                       Y_LABEL_INDEX)
y_labels = data_utils.get_y_labels(spreadsheet, X_LABEL_INDEX, Y_LABEL_INDEX)

season_day_count = np.full(len(SEASONS), 0, dtype=np.int_)
total_day_count = len(y_labels)
maximal_length_of_season = MAXIMUM_DAYS_IN_A_MONTH * MONTHS_PER_SEASON
season_daily_averages = [
    np.full(maximal_length_of_season, np.nan) for i in range(0, len(SEASONS))
]

for i, label in enumerate(y_labels):
    month_num_str = re.match(r'\d+\.(\d+)\.\d+', label).group(1)
    month_num_str = re.sub(r'^0+', '', month_num_str)
    daily_average = np.average(data_arr[i])
    month_num = int(month_num_str)
    season_num = MONTHS_TO_SEASONS[month_num]
    day_index = season_day_count[season_num]
    season_daily_averages[season_num][day_index] = daily_average
    season_day_count[season_num] += 1

fig, ax = plt.subplots(figsize=FIG_SIZE)
labels = [season.name for season in SEASONS]

for i in range(0, len(season_daily_averages)):
    arr = season_daily_averages[i]
    season_daily_averages[i] = arr[~np.isnan(arr)]

bplot1 = ax.boxplot(season_daily_averages,
                    vert=True,
                    patch_artist=True,
                    labels=labels)
ax.legend(loc="upper right")
plt.ylabel(Y_LABEL)
plt.title(CHART_TITLE)
plt.xticks(rotation=60, ha="right")
plt.show()
# plt.savefig(fname=chart_save_path)
