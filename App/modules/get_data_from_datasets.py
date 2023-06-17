import pandas as pd
import os
from IPython.display import display


# TODO make a function that check all file inside dataset
# TODO make a function to load all dataset into panda dataframe and return the dataframe


def collect_data():
    if os.path.exists("App/datasets/houses_dummy_datasets.json"):
        df = pd.read_json(os.path.join("App/datasets/houses_dummy_datasets.json"))

    # TODO return dataframe
    display(df)


if __name__ == "__main__":
    collect_data()
