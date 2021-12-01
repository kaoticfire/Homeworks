""" Helper functions for the user package and routes. """

from PIL import Image
from secrets import token_hex
from os import path

from werkzeug.datastructures import FileStorage
from website import mail
from flask_mail import Message
from flask import url_for, current_app


def save_picture(form_picture: FileStorage) -> str:
    """ Takes the picture name and path provided in the form and sets it to the users profile.
    
    Args:
        form_picture: The filename and path provided in the account form for a user.
    Return
        The filename of the picture to be attached to the users account.
    """
    random_hex = token_hex(8)
    _, f_ext = path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = path.join(current_app.root_path, 'static/pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user) -> None:
    """ This function sends a reset password link to the provided email. The link 
    contains a security token for authentication purposes.
    
    Args:
        user: the user email for existence to send.
    """
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request, then ignore this email but notify the website administrator. '''
    mail.send(msg)
