from flask import Blueprint, request, flash, redirect, jsonify, url_for, render_template
from website.models import Note, Needed
from website.ideas.forms import IdeaForm
from website import db
from flask_login import current_user, login_required
import json

ideas = Blueprint('ideas', __name__)


@ideas.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id or current_user.is_parent:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


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
        return redirect(url_for('ideas.home'))
    return render_template('create_idea.html', title='New Idea',
                           form=form, legend='New Idea')
