import numpy as np
import pathlib
import matplotlib.pyplot as plt
import data_utils
import argparse

# Data related
DATA_PATH = pathlib.Path("./data")
FACTUAL_WIND_SPEED_FILE = DATA_PATH.joinpath("vejaAtrumsFaktiskais.xlsx")
WINDGUST_SPEED_FILE = DATA_PATH.joinpath("vejaAtrumsBrazmas.xlsx")
CHART_TITLE = "Vidējais un maksimālais vēja ātrums 2023.gada augustā"
AVERAGE_SPEED_TITLE = "Vidējais"
WIND_GUST_TITLE = "Maksimālais"
X_LABEL = "Mērijumu datums"
Y_LABEL = "Vēja ātrums (m/s)"
X_LABEL_INDEX = 0
Y_LABEL_INDEX = 0

# Matplotlib configuration
BAR_WIDTH = 0.8
PX = 1 / plt.rcParams['figure.dpi']
FIG_SIZE = (1200 * PX, 1200 * PX)

# Showing or saving mode
parser = argparse.ArgumentParser(
    prog='first_exercise',
    description='Makes a double bar chart from xlsx files',
)
parser.add_argument(
    "--show",
    action=argparse.BooleanOptionalAction,
    help="Option for showing the resulting chart",
)
parser.add_argument(
    "--run",
    action=argparse.BooleanOptionalAction,
    help="Run the program without showing anything",
)
parser.add_argument(
    "--save",
    help="Option for saving the chart in the specified path",
)
args = parser.parse_args()
RUN = args.run
SAVE_FILE = True if args.save else False
SAVE_FILENAME = args.save
if SAVE_FILENAME:
    SAVE_FILEPATH = pathlib.Path(SAVE_FILENAME)
else:
    SAVE_FILEPATH = None
SHOW_CHART = True if args.show else False
if not SAVE_FILE and not SHOW_CHART and not RUN:
    parser.print_help()
    exit(0)

# This is where the ax labels are set
spreadsheet_files = {
    AVERAGE_SPEED_TITLE: FACTUAL_WIND_SPEED_FILE,
    WIND_GUST_TITLE: WINDGUST_SPEED_FILE
}
spreadsheets = {
    key: data_utils.get_work_sheet_by_index(val, index=0)
    for key, val in spreadsheet_files.items()
}
data_arrays = {
    key: data_utils.array_from_sheet(val, X_LABEL_INDEX, Y_LABEL_INDEX)
    for key, val in spreadsheets.items()
}
day_averages = np.array(
    [np.average(arr) for arr in data_arrays[AVERAGE_SPEED_TITLE]])
day_maximums = np.array([np.max(arr) for arr in data_arrays[WIND_GUST_TITLE]])

# I assume the spreadheet shape is the same
array_length = max([len(arr) for arr in data_arrays])
y_labels = data_utils.get_y_labels(spreadsheets[AVERAGE_SPEED_TITLE],
                                   X_LABEL_INDEX, Y_LABEL_INDEX)
fig, ax = plt.subplots(figsize=FIG_SIZE)
bottom_offset = day_averages
ax.bar(y_labels,
       day_maximums,
       BAR_WIDTH,
       label=WIND_GUST_TITLE,
       bottom=bottom_offset)
ax.bar(
    y_labels,
    day_averages,
    BAR_WIDTH,
    label=AVERAGE_SPEED_TITLE,
)

ax.legend(loc="upper right")
plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)
plt.title(CHART_TITLE)
plt.xticks(rotation=60, ha="right")
if SAVE_FILE:
    plt.savefig(fname=SAVE_FILEPATH)
if SHOW_CHART:
    plt.show()
