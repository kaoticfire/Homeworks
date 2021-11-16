from flask import Blueprint, request, flash, redirect, jsonify, url_for
from website.models import Note
from website import db, app, mail
from flask_login import current_user
from flask_mail import Message
from os import system
import json

ideas = Blueprint('ideas', __name__)


@ideas.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id or current_user.is_parent:
            note.is_active = False
            db.session.commit()

    return jsonify({})


@ideas.route('/report')
def export_list():
    notes = Note.query.filter(Note.is_active).all()
    flash('Exporting list now, please wait...', 'info')
    msg = Message('---Dinner Ideas---', sender=app.config['MAIL_USERNAME'], recipients=[current_user.email])
    with open('ideas.txt', 'a') as file:
        file.write('---Dinner Ideas---\n')
        for note in notes:
            file.write(str(note.data) + '\n')
            msg.body = str(note.data) + '\n'
            note.is_active = False
            db.session.commit()
    system(f'/usr/bin/lpr {file}')
    mail.send(msg)
    flash('Export complete,', 'success')

    return redirect(url_for('main.home'))
