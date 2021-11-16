from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from website.models import Note, Needed
from website import db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
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
    return render_template('home.html', user=current_user, notes=notes, )
