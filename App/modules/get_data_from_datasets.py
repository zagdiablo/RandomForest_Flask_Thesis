import pandas as pd
import os


# TODO make a function that check all file inside dataset
# TODO make a function to load all dataset into panda dataframe and return the dataframe


def datasets_to_database(dataset_file_name):
    if os.path.exists(f"App/datasets/{dataset_file_name}"):
        df = pd.read_json(os.path.join(f"App/datasets/{dataset_file_name}"))

    # TODO return dataframe
    for _, rs in df.iterrows():
        print(str(rs[0]))
        print(str(rs[1]))
        print(int(rs[2]))
        print(str(rs[3]))
        print(int(rs[4]))
        print(int(rs[5]))
        print(int(rs[6]))
        print(str(rs[7]))
        print(str(rs[8]))
        print(str(rs[9]))
