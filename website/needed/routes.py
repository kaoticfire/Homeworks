from flask import Blueprint, request, flash, redirect, jsonify, url_for, render_template
from website.models import Needed
from website import db, app, mail
from flask_login import current_user, login_required
from flask_mail import Message
from os import system
import json

needed = Blueprint('needed', __name__)


@needed.route('/supplies', methods=['GET', 'POST'])
@login_required
def supplies():
    page = request.args.get('page', 1, type=int)
    needed = Needed.query.paginate(page=page, per_page=10)
    if request.method == 'POST':
        need = request.form.get('supply')
        if len(need) < 5:
            flash('Supply is too short', 'error')
        else:
            new_supply = Needed(data=need, user_id=current_user.id)
            db.session.add(new_supply)
            db.session.commit()
            flash('Supply added!', category='success')
    return render_template('needed.html', user=current_user, needed=needed, )


@needed.route('/delete-supply', methods=['POST'])
def delete_note():
    supply = json.loads(request.data)
    supply_id = supply['supplyId']
    supply = Needed.query.get(supply_id)
    if supply:
        if supply.user_id == current_user.id or current_user.is_parent:
            supply.is_active = False
            db.session.commit()

    return jsonify({})


@needed.route('/supply_report')
def export_list():
    notes = Needed.query.filter(Needed.is_active).all()
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

    return redirect(url_for('needed.supplies'))
