import pandas as pd
import os
from os.path import isfile, join
import pathlib


# TODO create datasets reader
if os.name == "nt":
    ABSOLUTE_PATH = f"{pathlib.Path().absolute()}/App/datasets/"
else:
    ABSOLUTE_PATH = f"{pathlib.Path().absolute()}/App/datasets/"


def list_datasets():
    datasets = [
        ABSOLUTE_PATH + file
        for file in os.listdir(ABSOLUTE_PATH)
        if isfile(join(ABSOLUTE_PATH, file))
    ]

    return datasets


# TODO handle read excel data dynamically to match database
def read_and_reorder_datasets():
    datasets = ABSOLUTE_PATH + "DATA RUMAH TANGSEL.xlsx"

    if os.path.exists(datasets):
        df = pd.read_excel(os.path.join(datasets))

    datasets_column_title_list = df.columns.tolist()
    for title in datasets_column_title_list:
        print(title)

    for index, row in df.iterrows():
        value = row[datasets_column_title_list[1]]

        if not isinstance(value, float):
            print(value)
