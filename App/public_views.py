from flask import Blueprint, render_template, redirect, request, flash
from flask_login import current_user

import requests
import re

from .models import User, Rumah, Agen, Kecamatan
from . import db


public_views = Blueprint("public_views", __name__)

# TODO bikin dokumentasi untuk file ini
#################################################
# Functions
#################################################


def get_distance_api(tempat, tujuan):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={tempat}&destinations={tujuan}&key=AIzaSyAwqGQ5BbN_hu-bSFX7aHvqMDW2C2tK5Yo"
    print(url)

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    distance_data = dict(response.json())["rows"][0]["elements"][0]["distance"]["text"]
    try:
        distance = float(re.findall(r"\d+\.\d+", distance_data)[0])
    except IndexError:
        distance = "Tidak ada jalur darat."
    return distance


# TODO pengolahan data dan rekomendation system
# TODO flask query builder
def handle_query(
    the_user,
    user_is_authenticated,
    gaji_user,
    kecamatan,
    dropdown_lantai,
    dropdown_kamar_tidur,
    dropdown_kamar_mandi,
    checkbox_gym,
    checkbox_masjid,
    checkbox_taman,
    checkbox_playground,
    checkbox_kolam_renang,
):
    number = list("12345")
    query = Rumah.query.filter(Rumah.kecamatan == kecamatan)
    if user_is_authenticated:
        rekomendasi_harga_rumah = (((gaji_user * 40) / 100) * 12) * 30
        print(rekomendasi_harga_rumah)
        query = query.filter(Rumah.harga <= rekomendasi_harga_rumah)

    if dropdown_lantai in number:
        print("lantai")
        if int(dropdown_lantai) < 3:
            query = query.filter(Rumah.lantai == int(dropdown_lantai))
        else:
            query = query.filter(Rumah.lantai >= int(dropdown_lantai))
    if dropdown_kamar_tidur in number:
        print("kamar tidur")
        if int(dropdown_kamar_tidur) < 3:
            query = query.filter(Rumah.kamar_tidur == int(dropdown_kamar_tidur))
        else:
            query = query.filter(Rumah.kamar_tidur >= int(dropdown_kamar_tidur))
    if dropdown_kamar_mandi in number:
        if int(dropdown_kamar_mandi) < 3:
            query = query.filter(Rumah.kamar_mandi == int(dropdown_kamar_mandi))
        else:
            query = query.filter(Rumah.kamar_mandi >= int(dropdown_kamar_mandi))

    if checkbox_gym:
        print("gym")
        query = query.filter(Rumah.fasilitas.contains("gym"))
    if checkbox_masjid:
        print("masjid")
        query = query.filter(Rumah.fasilitas.contains("masjid"))
    if checkbox_taman:
        print("taman")
        query = query = query.filter(Rumah.fasilitas.contains("taman"))
    if checkbox_playground:
        print("playground")
        query = query.filter(Rumah.fasilitas.contains("playground"))
    if checkbox_kolam_renang:
        print("kolam renang")
        query = query.filter(Rumah.fasilitas.contains("kolam renang"))

    query_with_distances = {}
    if user_is_authenticated:
        query_results = query.order_by(Rumah.click_count.desc()).all()
        for query in query_results:
            query_cordinates = ",".join([query.latitude, query.longitude])
            distance = get_distance_api(the_user.alamat_tempat_kerja, query_cordinates)
            query_with_distances[distance] = query
        query_with_distances = dict(sorted(query_with_distances.items()))
    else:
        query_results = query.order_by(Rumah.click_count.desc()).all()
        for index, query in enumerate(query_results):
            query_with_distances[index] = query

    return query_with_distances


#################################################


#
#
# API untuk handle halaman home
@public_views.route("/", methods=["GET"])
def home_page():
    user_is_authenticated = current_user.is_authenticated

    return render_template(
        "public/home.html", user_is_authenticated=user_is_authenticated
    )


#
#
# API untuk handle halaman pencarian rumah
@public_views.route("/cari_rumah", methods=["GET"])
def cari_rumah_page():
    user_is_authenticated = current_user.is_authenticated
    if user_is_authenticated:
        the_user = User.query.get(current_user.get_id())
        status_profil_user = the_user.is_filled

    all_kecamatan = Kecamatan.query.all()
    all_agen = Agen.query.all()
    status_profil_user = None
    the_user = None
    query_rumah = None

    kecamatan = request.form.get("kecamatan")

    return render_template(
        "public/cari_rumah.html",
        user_is_authenticated=user_is_authenticated,
        all_kecamatan=all_kecamatan,
        all_agen=all_agen,
        kecamatan=kecamatan,
        status_profil_user=status_profil_user,
        query_rumah=query_rumah,
        the_user=the_user,
    )


@public_views.route("/handle_cari_rumah", methods=["POST"])
def handle_cari_rumah():
    user_is_authenticated = current_user.is_authenticated

    all_rumah = Rumah.query.all()
    all_kecamatan = Kecamatan.query.all()
    all_agen = Agen.query.all()
    gaji_user = None
    the_user = None
    status_profil_user = None

    kecamatan = request.form.get("search_bar_by_kecamatan")
    dropdown_lantai = request.form.get("dropdown_lantai")
    dropdown_kamar_tidur = request.form.get("dropdown_kamar_tidur")
    dropdown_kamar_mandi = request.form.get("dropdown_kamar_mandi")
    checkbox_gym = request.form.get("checkbox_gym")
    checkbox_masjid = request.form.get("checkbox_masjid")
    checkbox_taman = request.form.get("checkbox_taman")
    checkbox_playground = request.form.get("checkbox_playground")
    checkbox_kolam_renang = request.form.get("checkbox_kolam_renang")

    if user_is_authenticated:
        the_user = User.query.get(current_user.get_id())
        status_profil_user = the_user.is_filled
        gaji_user = the_user.range_gaji

    query_rumah = handle_query(
        the_user,
        user_is_authenticated,
        gaji_user,
        kecamatan,
        dropdown_lantai,
        dropdown_kamar_tidur,
        dropdown_kamar_mandi,
        checkbox_gym,
        checkbox_masjid,
        checkbox_taman,
        checkbox_playground,
        checkbox_kolam_renang,
    )

    return render_template(
        "public/cari_rumah.html",
        user_is_authenticated=user_is_authenticated,
        all_rumah=all_rumah,
        all_kecamatan=all_kecamatan,
        all_agen=all_agen,
        kecamatan_query=kecamatan,
        query_rumah=query_rumah,
        kecamatan=kecamatan,
        the_user=the_user,
        status_profil_user=status_profil_user,
    )


@public_views.route("/get_price_suggestion", methods=["POST"])
def get_price_suggestion():
    #####
    # TODO handle logika machine learning & query data hasil
    # TODO requirement: untuk user yang belum login range parameter gaji dan kontak sales rumah di tiadakan
    lantai = request.form.get("lantai")
    ukuran = request.form.get("ukuran")
    print(lantai, ukuran)
    #####

    return redirect("/cari_rumah")


#
#
# API untuk handle detail rumah
@public_views.route("/detail_rumah/<int:id>", methods=["GET"])
def detail_rumah(id):
    user_is_authenticated = current_user.is_authenticated
    detail_rumah = Rumah.query.get(id)
    fasilitas_rumah = detail_rumah.fasilitas
    jarak = None

    # add click count
    detail_rumah.click_count += 1
    db.session.commit()

    if user_is_authenticated:
        the_user = User.query.get(current_user.get_id())
        kordinat_rumah = ",".join([detail_rumah.latitude, detail_rumah.longitude])
        jarak = get_distance_api(the_user.alamat_tempat_kerja, kordinat_rumah)

    return render_template(
        "public/detail-rumah.html",
        detail_rumah=detail_rumah,
        fasilitas_rumah=fasilitas_rumah,
        jarak=jarak,
        user_is_authenticated=user_is_authenticated,
    )


#
#
# API untuk handle halaman tentang kami
@public_views.route("/about", methods=["GET"])
def about_page():
    user_is_authenticated = current_user.is_authenticated

    return render_template(
        "public/about.html", user_is_authenticated=user_is_authenticated
    )


#
#
# API untuk handle halaman kontak
@public_views.route("/contact", methods=["GET"])
def contact_page():
    user_is_authenticated = current_user.is_authenticated

    return render_template(
        "public/contact.html", user_is_authenticated=user_is_authenticated
    )
