# views handling halaman dashboard admin

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user


from .models import User, Kecamatan, Rumah, Agen, FixedBunga, GambarRumah
from .handle_image_upload import upload_image, delete_image
from . import db


admin_views = Blueprint("admin_views", __name__)


######################################
# functions
######################################


# fungsi untuk mengecek apakah user adalah admin atau tidak
def check_admin():
    user_object = User.query.get(current_user.get_id())
    return user_object.is_admin


######################################


# TODO add gambar upload functionality to tambah rumah and edit rumah


#
#
# API untuk handle admin dashboard, query jumlah rumah, kecamatan, user
# untuk di tampilkan di halaman dashboard admin
@admin_views.route("/admin_dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    count_rumah = Rumah.query.count()
    count_kecamatan = Kecamatan.query.count()
    count_user = User.query.count()
    admin_user = User.query.get(current_user.get_id())
    fixed_bunga = FixedBunga.query.get(1)

    return render_template(
        "admin/dashboard.html",
        admin_user=admin_user,
        count_rumah=count_rumah,
        count_kecamatan=count_kecamatan,
        count_user=count_user,
        fixed_bunga=fixed_bunga,
    )


# handle editing fixed bunga ke dalam database
@admin_views.route("/handle_edit_bunga", methods=["POST"])
@login_required
def handle_edit_bunga():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    fixed_bunga = request.form.get("fixed_bunga")

    to_edit_bunga = FixedBunga.query.get(1)

    if to_edit_bunga:
        to_edit_bunga.fixed_bunga = fixed_bunga
        db.session.commit()
        flash(
            f"berhasil mengedit fixed bunga menjadi {to_edit_bunga.fixed_bunga}",
            category="success",
        )
        return redirect("/admin_dashboard")

    flash(f"gagal mengedit fixed bunga")
    return redirect("/admin_dashboard")


#
#
# API untuk handle halaman kecamatan pada admin dashboard
# query semua kecamatan dalam database dan ditampilkan pada
# dahsboard admin
@admin_views.route("/admin_kecamatan", methods=["GEt"])
@login_required
def admin_kecamatan():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    all_kecamatan = Kecamatan.query.all()

    return render_template("admin/kecamatan.html", all_kecamatan=all_kecamatan)


# menampilkan halaman penambahan kecamatan pada dashboard admin
@admin_views.route("/tambah_kecamatan", methods=["GET"])
@login_required
def tambah_kecamatan():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/tambah-kecamatan.html")


# handle penambahan kecamatan pada halaman tambah kecamatan
@admin_views.route("/handle_tambah_kecamatan", methods=["POST"])
@login_required
def handle_tambah_kecamatan():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    kecamatan = request.form.get("kecamatan")

    to_add_kecamatan = Kecamatan(nama_kecamatan=kecamatan)
    db.session.add(to_add_kecamatan)
    db.session.commit()

    flash(f"Berhasil menambah kecamatan {kecamatan}", category="success")
    return redirect("/tambah_kecamatan")


# menampilkan halaman edit kecamatan pada admin dashboard
@admin_views.route("/edit_kecamatan/<int:id>", methods=["GET"])
@login_required
def edit_kecamatan(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_kecamatan = Kecamatan.query.get(id)

    return render_template(
        "admin/edit-kecamatan.html", to_edit_kecamatan=to_edit_kecamatan
    )


# handle edit kecamatan pada halaman edit kecamatan
@admin_views.route("/handle_edit_kecamatan/<int:id>", methods=["POST"])
@login_required
def handle_edit_kecamatan(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_kecamatan = Kecamatan.query.get(id)

    nama_kecamatan_baru = request.form.get("kecamatan")

    if to_edit_kecamatan:
        to_edit_kecamatan.nama_kecamatan = nama_kecamatan_baru
        db.session.commit()
        flash(
            f"berhasil mengedit data kecamatan {to_edit_kecamatan.nama_kecamatan}",
            category="success",
        )
        return redirect(f"/edit_kecamatan/{id}")

    flash(
        f"gagal mengedit data kecamatan {to_edit_kecamatan.nama_kecamatan}",
        category="error",
    )
    return redirect(f"/edit_kecamatan/{id}")


# handle penghapusan data kecamatan melalui admin dashboard
@admin_views.route("/delete_kecamatan/<int:id>", methods=["POST"])
def delete_kecamatan(id):
    to_delete_kecamatan = Kecamatan.query.get(id)
    if to_delete_kecamatan:
        flash(
            f"berhasil menghapus data kecamatan {to_delete_kecamatan.nama_kecamatan}",
            category="warning",
        )
        db.session.delete(to_delete_kecamatan)
        db.session.commit()
        return redirect("/admin_kecamatan")

    flash(
        f"gagal menghapus data kecamtan {to_delete_kecamatan.nama_kecamatan}",
        category="error",
    )
    return redirect("/admin_kecamatan")


#
#
# API untuk handle admin rumah
# mengqueru semua rumah dan ditampilkan di halaman dashboard admin
# pada menu rumah
@admin_views.route("/admin_rumah", methods=["GET"])
@login_required
def admin_rumah():
    if not check_admin():
        return redirect(url_for("admin_views_loggedin.profile_page"))

    all_rumah = Rumah.query.all()

    return render_template("admin/rumah.html", all_rumah=all_rumah)


# menampilkan halaman tambah rumah pada dashboard admin
@admin_views.route("/tambah_rumah", methods=["GET"])
@login_required
def tambah_rumah():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    all_rumah = Rumah.query.all()
    all_agen = Agen.query.all()
    all_kecamatan = Kecamatan.query.all()

    return render_template(
        "admin/tambah-rumah.html",
        all_rumah=all_rumah,
        all_agen=all_agen,
        all_kecamatan=all_kecamatan,
    )


# handle penambahan rummah pada dashboard admin
@admin_views.route("/handle_tambah_rumah", methods=["POST"])
@login_required
def handle_tambah_rumah():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    nama_perumahan = request.form.get("nama_perumahan")
    alamat = request.form.get("alamat")
    kecamatan = request.form.get("kecamatan")
    luas = request.form.get("luas")
    harga = request.form.get("harga")
    lantai = request.form.get("lantai")
    kamar_tidur = request.form.get("kamar_tidur")
    kamar_mandi = request.form.get("kamar_mandi")

    get_kontak_agen = request.form.get("kontak_agen").split(",")
    kontak_agen = get_kontak_agen[0]
    kontak_agen_id = int(get_kontak_agen[1])

    data_agen = Agen.query.get(kontak_agen_id)
    agen_nomor_telepon = data_agen.nomor_telepon
    agen_email = data_agen.email
    agen_whatsapp = data_agen.whatsapp

    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    deskripsi = request.form.get("deskripsi")
    gambar = request.files["gambar-rumah"]
    fasilitas = request.values.getlist("fasilitas")

    if gambar:
        if gambar == "":
            flash("Gambar Kosong", category="error")
            return redirect("/tambah_rumah")

        nama_file_gambar = upload_image(gambar, None)

    to_add_rumah = Rumah(
        nama_perumahan=nama_perumahan,
        alamat=alamat,
        kecamatan=kecamatan,
        luas=luas,
        harga=harga,
        lantai=lantai,
        kamar_tidur=kamar_tidur,
        kamar_mandi=kamar_mandi,
        kontak_agen=kontak_agen,
        kontak_agen_id=kontak_agen_id,
        agen_nomor_telepon=agen_nomor_telepon,
        agen_email=agen_email,
        agen_whatsapp=agen_whatsapp,
        latitude=latitude,
        longitude=longitude,
        deskripsi=deskripsi,
        fasilitas=", ".join(fasilitas),
    )
    db.session.add(to_add_rumah)
    db.session.commit()

    to_add_gambar = GambarRumah(
        nama_gambar=nama_file_gambar,
        rumah=Rumah.query.filter(Rumah.alamat == alamat).first().id,
    )
    db.session.add(to_add_gambar)
    db.session.commit()

    flash(f"Rumah {alamat} berhasil ditambah", category="success")
    return redirect("/tambah_rumah")


# menampilkan halaman edit rumah pada dashboard admin
@admin_views.route("/edit_rumah/<int:id>", methods=["GET"])
@login_required
def edit_rumah(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_rumah = Rumah.query.get(id)
    all_agen = Agen.query.all()
    all_kecamatan = Kecamatan.query.all()

    return render_template(
        "admin/edit-rumah.html",
        to_edit_rumah=to_edit_rumah,
        all_agen=all_agen,
        all_kecamatan=all_kecamatan,
    )


# handle pengeditan data rummah pada dashboard admin
@admin_views.route("/handle_edit_rumah/<int:id>", methods=["POST"])
@login_required
def handle_edit_rumah(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_rumah = Rumah.query.get(id)

    nama_perumahan = request.form.get("nama_perumahan")
    alamat = request.form.get("alamat")
    kecamatan = request.form.get("kecamatan")
    luas = request.form.get("luas")
    harga = request.form.get("harga")
    lantai = request.form.get("lantai")
    kamar_tidur = request.form.get("kamar_tidur")
    kamar_mandi = request.form.get("kamar_mandi")
    kontak_agen = request.form.get("kontak_agen")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    deskripsi = request.form.get("deskripsi")
    fasilitas = request.values.getlist("fasilitas")

    if to_edit_rumah:
        to_edit_rumah.nama_perumahan = nama_perumahan
        to_edit_rumah.alamat = alamat
        to_edit_rumah.kecamatan = kecamatan
        to_edit_rumah.luas = luas
        to_edit_rumah.harga = harga
        to_edit_rumah.lantai = lantai
        to_edit_rumah.kamar_tidur = kamar_tidur
        to_edit_rumah.kamar_mandi = kamar_mandi
        to_edit_rumah.kontak_agen = kontak_agen
        to_edit_rumah.latitude = latitude
        to_edit_rumah.longitude = longitude
        to_edit_rumah.gambar = to_edit_rumah.gambar
        to_edit_rumah.deskripsi = deskripsi
        to_edit_rumah.fasilitas = ", ".join(fasilitas)
        db.session.commit()
        flash(
            f"berhasil mengedit data rumah {to_edit_rumah.alamat}", category="warning"
        )
        return redirect(f"/edit_rumah/{id}")

    flash(f"gagal mengedit data rumah {to_edit_rumah.alamat}", category="error")
    return redirect(f"/edit_rumah/{id}")


@admin_views.route("/handle_tambah_gambar_rumah/<int:id>", methods=["POST"])
def handle_tambah_gambar_rumah(id):
    gambar = request.files["gambar-rumah"]

    nama_file_gambar = upload_image(gambar, None)
    to_add_gambar = GambarRumah(
        nama_gambar=nama_file_gambar,
        rumah=id,
    )
    db.session.add(to_add_gambar)
    db.session.commit()

    flash("Berhasil menambah gambar rumah")
    return redirect(f"/edit_rumah/{id}")


@admin_views.route("/handle_hapus_gambar_rumah/<int:id>", methods=["POST"])
def handle_hapus_gambar_rumah(id):
    id_gambar = int(request.form.get("id-gambar"))
    to_edit_rumah = Rumah.query.get(id)

    print(id_gambar)

    for gambar in to_edit_rumah.gambar:
        print(gambar.id, id_gambar)
        if gambar.id == id_gambar:
            to_delete_gambar = GambarRumah.query.get(gambar.id)
            print(f"{gambar.id} == {id_gambar}")
            flash(f"Berhasil menghapus gambar {gambar.nama_gambar}")
            delete_image(gambar.nama_gambar)
            db.session.delete(to_delete_gambar)
            db.session.commit()

    return redirect(f"/edit_rumah/{id}")


# handle penghapusan rumah pada dashboard admin
@admin_views.route("/delete_rumah/<int:id>", methods=["POST"])
@login_required
def delete_rumah(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_delete_rumah = Rumah.query.get(id)

    if to_delete_rumah:
        for gambar in to_delete_rumah.gambar:
            delete_image(gambar.nama_gambar)

        flash(
            f"berhasil menghapus data rumah {to_delete_rumah.alamat}",
            category="warning",
        )
        db.session.delete(to_delete_rumah)
        db.session.commit()
        return redirect("/admin_rumah")

    flash(f"gagal menghapus data rumah {to_delete_rumah.alamat}", category="error")
    return redirect("/admin_rumah")


#
#
# API untuk handle kontak agen
# query semua data agen untuk di tampilkan pada halaman
# dashboard admin pada menu rumah
@admin_views.route("/admin_kontak_agen", methods=["GET"])
@login_required
def admin_kontak_agen():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    all_agen = Agen.query.all()

    return render_template("admin/kontak-agen.html", all_agen=all_agen)


# menampilkan halaman penambahan admin pada admin dashboard
@admin_views.route("/tambah_agen", methods=["GET"])
@login_required
def tambah_agen():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/tambah-agen.html")


# handle penambahan agen pada dashboard admin
@admin_views.route("/handle_tambah_agen", methods=["POST"])
@login_required
def handle_tambah_agen():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    nama = request.form.get("nama_agen")
    nomor_telepon = request.form.get("nomor_telepon")
    email_agen = request.form.get("email")
    whatsapp_agen = request.form.get("whatsapp")

    to_add_agen = Agen(
        nama_agen=nama,
        nomor_telepon=nomor_telepon,
        email=email_agen,
        whatsapp=whatsapp_agen,
    )
    db.session.add(to_add_agen)
    db.session.commit()

    flash(f"Berhasil menambahkan agen {nama}")
    return redirect("/tambah_agen")


# menampilkan halaman edit agen pada dashboard admin
@admin_views.route("/edit_agen/<int:id>", methods=["GET"])
@login_required
def edit_agen(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_agen = Agen.query.get(id)

    return render_template("admin/edit-agen.html", to_edit_agen=to_edit_agen)


# handle pengeditan data agen pada dashboard admin
@admin_views.route("/handle_edit_agen/<int:id>", methods=["POST"])
@login_required
def handle_edit_agen(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_agen = Agen.query.get(id)

    nama_agen = request.form.get("nama_agen")
    nomor_telepon = request.form.get("nomor_telepon")
    email = request.form.get("email")
    whatsapp = request.form.get("whatsapp")

    if to_edit_agen:
        to_edit_agen.nama_agen = nama_agen
        to_edit_agen.nomor_telepon = nomor_telepon
        to_edit_agen.email = email
        to_edit_agen.whatsapp = whatsapp
        db.session.commit()

        flash(
            f"berhasil mengedit data agen {to_edit_agen.nama_agen}", category="warning"
        )
        return redirect(f"/edit_agen/{id}")

    flash(f"gagal mengedit data agen {to_edit_agen.nama_agen}", category="error")
    return redirect("/admin_agen")


# handle penghapusan data agen pada halaman dashboard admin
@admin_views.route("/delete_agen/<int:id>", methods=["POST"])
@login_required
def delete_agen(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_delete_agen = Agen.query.get(id)
    if to_delete_agen:
        flash(
            f"berhasil menghapus data agen {to_delete_agen.nama_agen}",
            category="warning",
        )
        db.session.delete(to_delete_agen)
        db.session.commit()
        return redirect("/admin_kontak_agen")

    flash(f"gagal menghapus data agen {to_delete_agen.nama_agen}", category="error")
    return redirect("/admin_kontak_agen")


#
#
# API untuk handle admin user
@admin_views.route("/admin_user", methods=["GET"])
@login_required
def admin_user():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    non_admin_user = User.query.filter(User.is_admin == False)

    return render_template("admin/user.html", non_admin_user=non_admin_user)


# untuk menampilkan halaman edit user pada dashboard admin
@admin_views.route("/edit_user/<int:id>", methods=["GET"])
@login_required
def edit_user(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_user = User.query.get(id)

    return render_template("admin/edit-user.html", to_edit_user=to_edit_user)


# handle pengeditan data user pada dashboard admin
@admin_views.route("/handle_edit_user/<int:id>", methods=["POST"])
@login_required
def handle_edit_user(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_user = User.query.get(id)

    nama_lengkap = request.form.get("nama_lengkap")
    email = request.form.get("email")
    range_gaji = request.form.get("range_gaji")

    if to_edit_user:
        to_edit_user.nama_lengkap = nama_lengkap
        to_edit_user.email = email
        to_edit_user.range_gaji = range_gaji
        db.session.commit()
        flash(
            f"berhasil edit data user {to_edit_user.nama_lengkap}", category="success"
        )
        return redirect(f"/edit_user/{id}")

    flash(f"gagal edit data user {to_edit_user.nama_lengkap}", category="error")
    return redirect(f"/edit_user/{id}")


# handle penghapusan user pada halaman dashboard admin
@admin_views.route("/delete_user/<int:id>", methods=["POST"])
@login_required
def delete_user(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_delete_user = User.query.get(id)

    if to_delete_user:
        flash(
            f"berhasil delete data user {to_delete_user.nama_lengkap}",
            category="success",
        )
        db.session.delete(to_delete_user)
        db.session.commit()
        return redirect("/admin_user")

    flash(f"gagal delete data user {to_delete_user.nama_lengkap}", category="error")
    return redirect("/admin_user")
