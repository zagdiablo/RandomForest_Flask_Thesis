from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user


from .models import User, Kecamatan, Rumah, Agen
from . import db


admin_views = Blueprint("admin_views", __name__)


######################################
# functions
######################################


def check_admin():
    user_object = User.query.get(current_user.get_id())
    return user_object.is_admin


######################################


# TODO add gambar upload functionality to tambah rumah and edit rumah


#
#
# API untuk handle admin dashboard
@admin_views.route("/admin_dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))
    count_rumah = Rumah.query.count()
    count_kecamatan = Kecamatan.query.count()
    count_user = User.query.count()
    admin_user = User.query.get(current_user.get_id())
    return render_template(
        "admin/dashboard.html",
        admin_user=admin_user,
        count_rumah=count_rumah,
        count_kecamatan=count_kecamatan,
        count_user=count_user,
    )


#
#
# API untuk handle admin kecamatan
@admin_views.route("/admin_kecamatan", methods=["GEt"])
@login_required
def admin_kecamatan():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    all_kecamatan = Kecamatan.query.all()

    return render_template("admin/kecamatan.html", all_kecamatan=all_kecamatan)


@admin_views.route("/tambah_kecamatan", methods=["GET"])
@login_required
def tambah_kecamatan():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/tambah-kecamatan.html")


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


@admin_views.route("/edit_kecamatan/<int:id>", methods=["GET"])
@login_required
def edit_kecamatan(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_kecamatan = Kecamatan.query.get(id)

    return render_template(
        "admin/edit-kecamatan.html", to_edit_kecamatan=to_edit_kecamatan
    )


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
@admin_views.route("/admin_rumah", methods=["GET"])
@login_required
def admin_rumah():
    if not check_admin():
        return redirect(url_for("admin_views_loggedin.profile_page"))

    all_rumah = Rumah.query.all()

    return render_template("admin/rumah.html", all_rumah=all_rumah)


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
    kontak_agen = request.form.get("kontak_agen")

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
    )
    db.session.add(to_add_rumah)
    db.session.commit()

    flash(f"Rumah {alamat} berhasil ditambah", category="success")
    return redirect("/tambah_rumah")


@admin_views.route("/edit_rumah/<int:id>", methods=["GET"])
@login_required
def edit_rumah(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_rumah = Rumah.query.get(id)
    all_agen = Agen.query.all()

    return render_template(
        "admin/edit-rumah.html", to_edit_rumah=to_edit_rumah, all_agen=all_agen
    )


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
        db.session.commit()
        flash(
            f"berhasil mengedit data rumah {to_edit_rumah.alamat}", category="warning"
        )
        return redirect(f"/edit_rumah/{id}")

    flash(f"gagal mengedit data rumah {to_edit_rumah.alamat}", category="error")
    return redirect(f"/edit_rumah/{id}")


@admin_views.route("/delete_rumah/<int:id>", methods=["POST"])
@login_required
def delete_rumah(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_delete_rumah = Rumah.query.get(id)

    if to_delete_rumah:
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
@admin_views.route("/admin_kontak_agen", methods=["GET"])
@login_required
def admin_kontak_agen():
    if not check_admin():
        return redirect(url_for("admin_views_loggedin.profile_page"))

    all_agen = Agen.query.all()

    return render_template("admin/kontak-agen.html", all_agen=all_agen)


@admin_views.route("/tambah_agen", methods=["GET"])
@login_required
def tambah_agen():
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    return render_template("admin/tambah-agen.html")


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


@admin_views.route("/edit_agen/<int:id>", methods=["GET"])
@login_required
def edit_agen(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_agen = Agen.query.get(id)

    return render_template("admin/edit-agen.html", to_edit_agen=to_edit_agen)


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
        return redirect(url_for("admin_views_loggedin.profile_page"))

    non_admin_user = User.query.filter(User.is_admin == False)

    return render_template("admin/user.html", non_admin_user=non_admin_user)


@admin_views.route("/edit_user/<int:id>", methods=["GET"])
@login_required
def edit_user(id):
    if not check_admin():
        return redirect(url_for("public_views_loggedin.profile_page"))

    to_edit_user = User.query.get(id)

    return render_template("admin/edit-user.html", to_edit_user=to_edit_user)


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
