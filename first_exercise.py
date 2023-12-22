import numpy as np
import openpyxl
import pathlib
import matplotlib.pyplot as plt

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

# Type shorthands for convinience
Float2DArray = np.ndarray[tuple[int, int], np.float_]
Worksheet = openpyxl.worksheet.worksheet.Worksheet


def get_work_sheet_by_index(file: pathlib.Path, index: int) -> Worksheet:
    book = openpyxl.load_workbook(file)
    sheet = book.worksheets[index]
    return sheet


def get_y_labels(sheet: Worksheet, x_label_index: int,
                 y_label_index) -> list[str]:
    row_values = [[cell.value for cell in row] for row in sheet.rows]
    labels = [row[x_label_index] for row in row_values]
    return labels[y_label_index + 1:] if len(row_values) >= (y_label_index +
                                                             2) else []


def get_x_labels(sheet: Worksheet, x_label_index: int,
                 y_label_index) -> list[str]:
    row_values = [[cell.value for cell in row] for row in sheet.rows]
    label_row_values = row_values[y_label_index] if len(row_values) >= (
        y_label_index + 1) else None
    if label_row_values is not None:
        labels = [cell_value for cell_value in label_row_values]
        labels = labels[x_label_index + 1:] if len(labels) >= (x_label_index +
                                                               1 + 1) else []
    else:
        labels = []
    return labels


def fill_2d_array_from_worksheet(arr: Float2DArray, sheet: Worksheet,
                                 x_label_index: int,
                                 y_label_index: int) -> Float2DArray:
    rows = [row for row in sheet.rows]
    for i, row in enumerate(rows[y_label_index + 1:]):
        for k, cell in enumerate(row[x_label_index + 1:]):
            arr[i, k] = cell.value
    return arr


def worksheet_array_shape(sheet: Worksheet, x_label_index: int,
                          y_label_index: int) -> tuple[int, int]:
    row_generator = sheet.rows
    rows = [row for row in row_generator]
    row_count = len(rows)
    column_count = len(rows[0]) if row_count > 0 else 0
    shape = (row_count - (y_label_index + 1),
             column_count - (x_label_index + 1))
    return shape


def array_from_sheet(sheet: Worksheet, x_label_index: int,
                     y_label_index: int) -> Float2DArray:
    shape = worksheet_array_shape(sheet, X_LABEL_INDEX, Y_LABEL_INDEX)
    arr = np.empty(shape, dtype=np.float_)
    filled_arr = fill_2d_array_from_worksheet(arr, sheet, x_label_index,
                                              y_label_index)
    return filled_arr


# This is where the ax labels are set
spreadsheet_files = {
    "Factual speed": FACTUAL_WIND_SPEED_FILE,
    "Wind gusts": WINDGUST_SPEED_FILE
}
spreadsheets = [
    get_work_sheet_by_index(file, index=0)
    for file in spreadsheet_files.values()
]
data_arrays = [
    array_from_sheet(sheet, X_LABEL_INDEX, Y_LABEL_INDEX)
    for sheet in spreadsheets
]

# I assume the spreadheet shape is the same
array_length = max([len(arr) for arr in data_arrays])
y_labels = get_y_labels(spreadsheets[0], X_LABEL_INDEX, Y_LABEL_INDEX)
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
