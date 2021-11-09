from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from os import system
from flask_login import login_required, current_user
from .models import Note, Chore
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    notes = Note.query.all()
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 5:
            flash('Idea is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Idea added!', category='success')
    return render_template('home.html', user=current_user, notes=notes)


@views.route('/chore', methods=['GET', 'POST'])
@login_required
def chore():
    chores = Chore.query.all()
    if request.method == 'POST':
        chore = request.form.get('chore')
        if len(chore) < 5:
            flash('Idea is too short', category='error')
        else:
            new_chore = Chore(data=chore, user_id=current_user.id)
            db.session.add(new_chore)
            db.session.commit()
            flash('Chore added!', category='success')
    return render_template('chore.html', user=current_user, chores=chores)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id or current_user.is_parent:
            note.is_active = False
            db.session.commit()

    return jsonify({})


@views.route('/delete-chore', methods=['POST'])
@login_required
def delete_chore():
    chore = json.loads(request.data)
    chore_id = chore['choreId']
    chore = chore.query.get(chore_id)
    if chore:
        if chore.user_id == current_user.id or current_user.is_parent:
            chore.is_active = False
            db.session.commit()

    return jsonify({})


@views.route('/report')
@login_required
def export_list():
    notes = Note.query.filter(Note.is_active).all()
    flash('Exporting list now, please wait...', category='info')
    with open('ideas.txt', 'a') as file:
        file.write('---Dinner Ideas---\n')
        for note in notes:
            file.write(str(note.data) + '\n')
            note.is_active = False
            db.session.commit()
    system(f'/usr/bin/lpr {file}')
    flash('Export complete,', category='success')

    return redirect(url_for('views.home'))
