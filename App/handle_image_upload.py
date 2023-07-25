import random
import os

from . import db
from . import app


ALLOWED_EXTENTIONS = set(["png", "jpg", "jpeg", "gif"])


def file_is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENTIONS


def upload_image(image_file, to_edit_query_object):
    if image_file and file_is_allowed(image_file.filename):
        image_file_name = f"{random.randint(1000000, 9999999)}_{image_file.filename}"

        if to_edit_query_object:
            # TODO change local server save
            if os.name == "nt":
                # windows path
                image_file.save(
                    f'{app.config["UPLOAD_IMAGE_FOLDER"]}/{image_file_name}'
                )
                to_edit_query_object.gambar = image_file_name
                db.session.commit()
            else:
                # python anywhere save
                image_file.save(
                    os.path.join(app.config["UPLOAD_IMAGE_FOLDER"], image_file_name)
                )
                to_edit_query_object.gambar = image_file_name
                db.session.commit()

            return

        if os.name == "nt":
            # windows path
            image_file.save(f'{app.config["UPLOAD_IMAGE_FOLDER"]}/{image_file_name}')
        else:
            # python anywhere save
            image_file.save(
                os.path.join(app.config["UPLOAD_IMAGE_FOLDER"], image_file_name)
            )
        return image_file_name


def delete_image(image_file_name):
    if image_file_name:
        try:
            if os.name == "nt":
                # windows path
                os.remove(f'{app.config["UPLOAD_IMAGE_FOLDER"]}/{image_file_name}')
            else:
                # python anywhere delete path
                os.remove(
                    os.path.join(app.config["UPLOAD_IMAGE_FOLDER"], image_file_name)
                )
        except FileNotFoundError:
            return
    return
