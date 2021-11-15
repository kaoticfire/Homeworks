from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from os import system, path
from flask_login import login_required, current_user
from .models import Note, Chore
from .forms import UpdateAccountForm
from . import db, app, mail
import json
from PIL import Image
from secrets import token_hex
from flask_mail import Message

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
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
            db.session.add(new_note)
            db.session.commit()
            flash('Idea added!', category='success')
    return render_template('home.html', user=current_user, notes=notes, )


@views.route('/chore', methods=['GET', 'POST'])
def chore():
    chores = Chore.query.all()
    if request.method == 'POST':
        task = request.form.get('chore')
        if len(task) < 5:
            flash('Idea is too short', 'error')
        else:
            new_chore = Chore(data=chore, user_id=current_user.id)
            db.session.add(new_chore)
            db.session.commit()
            flash('Chore added!', 'success')
    return render_template('chore.html', user=current_user, chores=chores)


@views.route('/delete-note', methods=['POST'])
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
def delete_chore():
    task = json.loads(request.data)
    chore_id = task['choreId']
    task = task.query.get(chore_id)
    if task:
        if chore.user_id == current_user.id or current_user.is_parent:
            chore.is_active = False
            db.session.commit()

    return jsonify({})


@views.route('/report')
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

    return redirect(url_for('views.home'))


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


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.email.data = current_user.email
    img_file = url_for('static', filename='/pics/' + current_user.img_file)
    return render_template('account.html', title='Account',
                           image_file=img_file, form=form)
