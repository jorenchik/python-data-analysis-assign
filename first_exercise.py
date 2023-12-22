import numpy as np
import pathlib
import matplotlib.pyplot as plt
import data_utils

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
CHART_FILENAME = "first_exercise.png"
CHART_SAVE_PATH = pathlib.Path(CHART_FILENAME)
BAR_WIDTH = 0.8
PX = 1 / plt.rcParams['figure.dpi']
FIG_SIZE = (1200 * PX, 1200 * PX)

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
plt.savefig(fname=CHART_SAVE_PATH)
