from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user

import requests
import re

from .models import User, Rumah, Agen, Kecamatan, FixedBunga
from . import db


public_views = Blueprint("public_views", __name__)

# TODO bikin dokumentasi untuk file ini
#################################################
# Functions
#################################################


# fungsi untuk mendapatkan perhitungan jarak dari google API
def get_distance_api(tempat, tujuan, user_is_authenticated):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={tempat}&destinations={tujuan}&key=AIzaSyAwqGQ5BbN_hu-bSFX7aHvqMDW2C2tK5Yo"

    payload = {}
    headers = {}

    if user_is_authenticated:
        response = requests.request("GET", url, headers=headers, data=payload)
        distance_data = dict(response.json())["rows"][0]["elements"][0]["distance"][
            "text"
        ]
        try:
            distance = float(re.findall(r"\d+\.\d+", distance_data)[0])
        except IndexError:
            distance = "Tidak ada jalur darat."
        return distance
    return None


# fungsi untuk mencari data dalam database menggunakan parameter query
# yang didapat dari halaman cari_rumah.html
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

    # query rumah berdasarkan kecamatan dan fasilitas yang di passing dari halaman cari rumah
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
    # jika user telah login, query dan hitung jarak menggunakan fungsi get_distance_api
    if user_is_authenticated:
        query_results = query.order_by(Rumah.click_count.desc()).all()
        for query in query_results:
            query_cordinates = ",".join([query.latitude, query.longitude])
            distance = get_distance_api(
                the_user.alamat_tempat_kerja, query_cordinates, user_is_authenticated
            )
            query_with_distances[distance] = query
        # sorted(query_with_distances.items()) mengurutkan hasil query berdasarkan jarak
        query_with_distances = dict(sorted(query_with_distances.items()))
    # jika tidak isi jarak dengan angka index saja, dan tidak ditampilkan pada halaman hasil pencarian
    else:
        # click_count.desc() query data yang di urutkan berdasarkan click count terbanyak
        query_results = query.order_by(Rumah.click_count.desc()).all()
        for index, query in enumerate(query_results):
            query_with_distances[index] = query

    # return data hasil query database
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
    # jika user login maka query data user
    user_is_authenticated = current_user.is_authenticated

    # query list kecamatan dan agen
    all_kecamatan = Kecamatan.query.all()
    all_agen = Agen.query.all()
    all_rumah = Rumah.query.filter(Rumah.kamar_mandi > 0)
    status_profil_user = None
    the_user = None
    query_results = all_rumah.order_by(Rumah.click_count.desc()).all()

    query_rumah = {}
    if user_is_authenticated:
        the_user = User.query.get(current_user.get_id())
        status_profil_user = the_user.is_filled

        for rumah in query_results:
            query_cordinates = ",".join([rumah.latitude, rumah.longitude])
            distance = get_distance_api(
                the_user.alamat_tempat_kerja, query_cordinates, user_is_authenticated
            )
            query_rumah[distance] = rumah
        # sorted(query_with_distances.items()) mengurutkan hasil query berdasarkan jarak
        query_rumah = dict(sorted(query_rumah.items()))
    else:
        # query semua rumah
        for index, rumah in enumerate(query_results):
            query_rumah[index] = rumah

    # manmpilkan halaman cari rumah dengan hasil query yg telah di dapat
    return render_template(
        "public/cari_rumah.html",
        user_is_authenticated=user_is_authenticated,
        all_kecamatan=all_kecamatan,
        all_agen=all_agen,
        status_profil_user=status_profil_user,
        query_rumah=query_rumah,
        the_user=the_user,
    )


# handle query rumah berdasarkan detail dan parameter pencarian yang ada di halaman cari rumah
# mengecek parameter pencarian seperti fasilitas, lantai, kamar mandi, dan kamar tidur
# di olang menggunakan fungsi handle_query() lalu di tampilkan hasil querinya
# pada halama cari rumah
@public_views.route("/handle_cari_rumah", methods=["POST"])
def handle_cari_rumah():
    # cek user login atau tidak
    user_is_authenticated = current_user.is_authenticated

    # qery semua data rumah dari database
    all_rumah = Rumah.query.all()
    all_kecamatan = Kecamatan.query.all()
    all_agen = Agen.query.all()
    gaji_user = None
    the_user = None
    status_profil_user = None

    # penarikan parameter dari form pencarian rumah
    kecamatan = request.form.get("search_bar_by_kecamatan")
    dropdown_lantai = request.form.get("dropdown_lantai")
    dropdown_kamar_tidur = request.form.get("dropdown_kamar_tidur")
    dropdown_kamar_mandi = request.form.get("dropdown_kamar_mandi")
    checkbox_gym = request.form.get("checkbox_gym")
    checkbox_masjid = request.form.get("checkbox_masjid")
    checkbox_taman = request.form.get("checkbox_taman")
    checkbox_playground = request.form.get("checkbox_playground")
    checkbox_kolam_renang = request.form.get("checkbox_kolam_renang")

    # jika user login maka query data user dari database
    if user_is_authenticated:
        the_user = User.query.get(current_user.get_id())
        status_profil_user = the_user.is_filled
        gaji_user = the_user.range_gaji

    # pemanggilan fungsi handle_query() untuk query data rumah dengan parameter yang diinginkan
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

    # tampilkan hasil query ke halaman cari rumah
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


#
#
# API untuk handle detail rumah
@public_views.route("/detail_rumah/<int:id>/<int:from_cari_rumah>", methods=["GET"])
def detail_rumah(id, from_cari_rumah):
    # query data detail dan fasilitas rumah
    user_is_authenticated = current_user.is_authenticated
    detail_rumah = Rumah.query.get(id)
    fasilitas_rumah = detail_rumah.fasilitas
    fixed_bunga = FixedBunga.query.get(1)
    jarak = None
    cicilan = None

    # jika user login maka query data user
    if user_is_authenticated:
        the_user = User.query.get(current_user.get_id())
        kordinat_rumah = ",".join([detail_rumah.latitude, detail_rumah.longitude])
        jarak = get_distance_api(
            the_user.alamat_tempat_kerja, kordinat_rumah, user_is_authenticated
        )

    # jika user click detail rumah pada halaman cari rumah maka dihitung click count
    # pengurutan rumah rekomendasi jika user tidak login adalah berdasarkan click count
    # urutan paling atas adalah rumah yang paling banyak click count nya
    if from_cari_rumah == 1:
        detail_rumah.click_count += 1
        db.session.commit()

        return redirect(
            url_for(
                "public_views.detail_rumah",
                id=id,
                from_cari_rumah=0,
                detail_rumah=detail_rumah,
                fasilitas_rumah=fasilitas_rumah,
                jarak=jarak,
                user_is_authenticated=user_is_authenticated,
                cicilan=cicilan,
                fixed_bunga=fixed_bunga,
            )
        )

    # menampilkan data hasil query pada halaman detail rumah
    return render_template(
        f"public/detail-rumah.html",
        detail_rumah=detail_rumah,
        fasilitas_rumah=fasilitas_rumah,
        jarak=jarak,
        user_is_authenticated=user_is_authenticated,
        cicilan=cicilan,
        fixed_bunga=fixed_bunga,
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
