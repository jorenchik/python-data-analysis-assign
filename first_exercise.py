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
    "Factual speed": FACTUAL_WIND_SPEED_FILE,
    "Wind gusts": WINDGUST_SPEED_FILE
}
spreadsheets = [
    data_utils.get_work_sheet_by_index(file, index=0)
    for file in spreadsheet_files.values()
]
data_arrays = [
    data_utils.array_from_sheet(sheet, X_LABEL_INDEX, Y_LABEL_INDEX)
    for sheet in spreadsheets
]

# I assume the spreadheet shape is the same
array_length = max([len(arr) for arr in data_arrays])
y_labels = data_utils.get_y_labels(spreadsheets[0], X_LABEL_INDEX,
                                   Y_LABEL_INDEX)
averages = np.empty(shape=(len(data_arrays), array_length))
for i, arr in enumerate(data_arrays):
    row_average_values = np.array(
        [np.average(row_values) for row_values in arr])
    averages[i] = row_average_values

fig, ax = plt.subplots(figsize=FIG_SIZE)
bottom = np.zeros(array_length)
for title, data in zip(spreadsheet_files.keys(), averages):
    ax.bar(y_labels, data, BAR_WIDTH, label=title, bottom=bottom)
    bottom += data
ax.legend(loc="upper right")
plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)
plt.title(CHART_TITLE)
plt.xticks(rotation=60, ha="right")
if SAVE_FILE:
    plt.savefig(fname=SAVE_FILEPATH)
if SHOW_CHART:
    plt.show()
