from PIL import Image
from secrets import token_hex
from os import path
from website import app, mail
from flask_mail import Message
from flask import url_for


def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = path.join(app.root_path, 'static/pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request, then ignore this email but notify the website administrator.'''
    mail.send(msg)
