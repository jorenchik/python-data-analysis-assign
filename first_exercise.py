import numpy as np
import openpyxl
import pathlib

DATA_PATH = pathlib.Path("./data")
FACTUAL_WIND_SPEED_FILE = DATA_PATH.joinpath("vejaAtrumsFaktiskais.xlsx")
WINDGUST_SPEED_FILE = DATA_PATH.joinpath("vejaAtrumsBrazmas.xlsx")
X_LABEL_INDEX = 0
Y_LABEL_INDEX = 0

Float2DArray = np.ndarray[tuple[int, int], np.float_]
Worksheet = openpyxl.worksheet.worksheet.Worksheet


def get_work_sheet_by_index(file: pathlib.Path, index: int) -> Worksheet:
    book = openpyxl.load_workbook(file)
    sheet = book.worksheets[index]
    return sheet


def get_x_labels(sheet: Worksheet, x_label_index: int,
                 y_label_index) -> list[str]:
    row_values = [[cell.value for cell in row] for row in sheet.rows]
    labels = [row[x_label_index] for row in row_values]
    return labels[y_label_index + 1:] if len(row_values) >= (y_label_index +
                                                             2) else []


def get_y_labels(sheet: Worksheet, x_label_index: int,
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


sheet = get_work_sheet_by_index(FACTUAL_WIND_SPEED_FILE, index=0)
shape = worksheet_array_shape(sheet, X_LABEL_INDEX, Y_LABEL_INDEX)
arr = np.empty(shape, dtype=np.float_)
filled_arr = fill_2d_array_from_worksheet(arr, sheet, X_LABEL_INDEX,
                                          Y_LABEL_INDEX)
x_labels = get_x_labels(sheet, X_LABEL_INDEX, Y_LABEL_INDEX)
y_labels = get_y_labels(sheet, X_LABEL_INDEX, Y_LABEL_INDEX)
