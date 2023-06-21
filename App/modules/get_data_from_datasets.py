import json
import os


# TODO make a function that check all file inside dataset
# TODO make a function to load all dataset into panda dataframe and return the dataframe


def collect_data():
    with open("./houses_dummy_datasets.json", "r") as dataset:
        list_rumah = json.load(dataset)

    for (
        alamat,
        nama_perumahan,
        luas,
        harga,
        lantai,
        jumlah_kamar_tidur,
        jumlah_kamar_mandi,
        kecamatan,
        kordinat,
        kontak_agen_penjual,
    ) in list_rumah:
        print(
            alamat,
            nama_perumahan,
            luas,
            harga,
            lantai,
            jumlah_kamar_tidur,
            jumlah_kamar_mandi,
            kecamatan,
            kordinat,
            kontak_agen_penjual,
        )


if __name__ == "__main__":
    collect_data()
