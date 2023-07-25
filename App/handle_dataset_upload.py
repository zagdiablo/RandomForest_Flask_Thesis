import pandas as pd
import os
import pathlib

from . import db
from .models import Rumah, Kecamatan, Agen


ALLOWED_EXTENTIONS = set(["xlsx", "xls"])


def file_is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENTIONS


def upload_dataset(dataset_file):
    if dataset_file and file_is_allowed(dataset_file.filename):
        if dataset_file.filename != "":
            try:
                df = pd.read_excel(dataset_file)
                df.to_excel(
                    f"{pathlib.Path().absolute()}/App/datasets/{dataset_file.filename}",
                    index=False,
                )
            except Exception as e:
                return False, f"Gagal memproses file {str(e)}"
        else:
            return False, f"Hanya file bertipe .xlsx yang dapat di upload."

    return True, "Berhasil mengupload file dataset."


def delete_dataset(dataset_file):
    if dataset_file:
        try:
            os.remove(
                f"{pathlib.Path().absolute()}/App/datasets/{dataset_file.filename}"
            )
        except FileNotFoundError:
            return False
    return True


def add_dataset_kecamatan(df, datasets_column_title_list):
    for _, row in df.iterrows():
        if isinstance(row[datasets_column_title_list[5]], float):
            continue

        to_check_kecamatan = Kecamatan.query.filter_by(
            nama_kecamatan=str(row[datasets_column_title_list[5]]).lower()
        ).first()

        if not to_check_kecamatan:
            new_kecamatan = Kecamatan(nama_kecamatan=row[datasets_column_title_list[5]])
            db.session.add(new_kecamatan)
    db.session.commit()


def add_dataset_kontak(df, datasets_column_title_list):
    for _, row in df.iterrows():
        if isinstance(row[datasets_column_title_list[11]], float):
            continue

        to_check_agen = Agen.query.filter_by(
            nama_agen=str(row[datasets_column_title_list[11]]).lower()
        ).first()

        if not to_check_agen:
            new_agen = Agen(
                nama_agen=row[datasets_column_title_list[11]],
                nomor_telepon="",
                email="",
                whatsapp="",
            )
            db.session.add(new_agen)
        db.session.commit()


# TODO create database input
def input_dataset_to_database(dataset_file):
    path_to_file = f"{pathlib.Path().absolute()}/App/datasets/{dataset_file.filename}"

    if os.path.exists(path_to_file):
        try:
            df = pd.read_excel(path_to_file)
        except Exception as e:
            print(e)
            return

    datasets_column_title_list = df.columns.tolist()

    add_dataset_kecamatan(df, datasets_column_title_list)
    add_dataset_kontak(df, datasets_column_title_list)

    for index, row in df.iterrows():
        nama_perumahan = row[datasets_column_title_list[1]]
        alamat = row[datasets_column_title_list[2]]
        latitude = row[datasets_column_title_list[3]]
        longitude = row[datasets_column_title_list[4]]
        kecamatan = row[datasets_column_title_list[5]]
        luas = row[datasets_column_title_list[6]]
        harga = row[datasets_column_title_list[7]]
        lantai = row[datasets_column_title_list[8]]
        kamar_tidur = row[datasets_column_title_list[9]]
        kamar_mandi = row[datasets_column_title_list[10]]
        nama_kontak_person = row[datasets_column_title_list[11]]
        nomor_hp = row[datasets_column_title_list[12]]
        fasilitas = row[datasets_column_title_list[13]]
        deskripsi_rumah = row[datasets_column_title_list[14]]

        if isinstance(nama_perumahan, float):
            continue

        to_add_rumah = Rumah(
            nama_perumahan=nama_perumahan,
            alamat=alamat,
            harga=harga,
            kecamatan=kecamatan,
            latitude=latitude,
            longitude=longitude,
            kontak_agen=nama_kontak_person,
            kontak_agen_id=0,
            agen_nomor_telepon=nomor_hp,
            agen_email="",
            agen_whatsapp="",
            categori_fasilitas="",
            fasilitas=fasilitas,
            luas=luas,
            lantai=lantai,
            kamar_tidur=kamar_tidur,
            kamar_mandi=kamar_mandi,
            njop=0,
            click_count=0,
            deskripsi=deskripsi_rumah,
        )
        db.session.add(to_add_rumah)
        db.session.commit()

    return
