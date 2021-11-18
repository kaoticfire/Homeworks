from flask import Blueprint, request, flash, redirect, jsonify, url_for, current_app, render_template
from website.models import Note, Needed
from website.ideas.forms import IdeaForm
from website import db, mail
from flask_login import current_user, login_required
from flask_mail import Message
from os import system
import json

ideas = Blueprint('ideas', __name__)


@ideas.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    supply = Needed.query.filter_by(data=note.data)
    if note:
        if note.user_id == current_user.id or current_user.is_parent:
            note.is_active = False
            db.session.delete(supply)
            db.session.commit()
    return jsonify({})


@ideas.route('/report')
def export_list():
    notes = Note.query.filter(Note.is_active).all()
    flash('Exporting list now, please wait...', 'info')
    msg = Message('---Dinner Ideas---', sender=current_app.config['MAIL_USERNAME'], recipients=[current_user.email])
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

    return redirect(url_for('ideas.home'))


@ideas.route('/', methods=['GET', 'POST'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    notes = Note.query.paginate(page=page, per_page=5)
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 5:
            flash('Idea is too short', 'error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            new_supply = Needed(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.add(new_supply)
            db.session.commit()
            flash('Idea added!', category='success')
    return render_template('ideas.html', user=current_user, notes=notes, )


@ideas.route("/new_idea", methods=['GET', 'POST'])
@login_required
def new_idea():
    form = IdeaForm()
    if form.validate_on_submit():
        note = Note(data=form.title.data, url=form.recipe.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash('Your idea has been added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_idea.html', title='New Idea',
                           form=form, legend='New Idea')
