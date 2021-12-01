""" All routes pertaining to the supply package. """
from flask import Blueprint, request, flash, redirect, jsonify, url_for, render_template, current_app
from website.models import Needed, Note
from website.supplies.forms import SupplyForm
from website import db, mail
from flask_login import current_user, login_required
from flask_mail import Message
from os import system
from json import loads

supply = Blueprint('supplies', __name__)


@supply.route('/supplies', methods=['GET', 'POST'])
@login_required
def supplies():
    """ List and display active supplies needed. """
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
    return render_template('supplies.html', user=current_user, needed=needed, )


@supply.route("/new_supply", methods=['GET', 'POST'])
def new_idea():
    """ Custom form to add a new supply needed. """
    form = SupplyForm()
    if form.validate_on_submit():
        item = Needed(data=form.supply.data, author=current_user)
        db.session.add(item)
        db.session.commit()
        flash('Your item has been added!', 'success')
        return redirect(url_for('supply.supplies'))
    return render_template('create_supply.html', title='New Supply Item',
                           form=form, legend='New Supply Item')


@supply.route('/delete-supply', methods=['POST'])
def delete_supply():
    """ Gets the id of the current supply need and removes from database. """
    supplys = loads(request.data)
    supply_id = supplys['supplyId']
    supplys = Needed.query.get(supply_id)
    if supply:
        if supplys.user_id == current_user.id or current_user.is_parent:
            db.session.delete(supplys)
            db.session.commit()
    return jsonify({})


@supply.route('/supply_report')
def export_list():
    """ Take supply need list and write to file for printing as well as attempt to send an email pertaining to. """
    items = Note.query.filter(Note.is_active).all()
    needs = Needed.query.filter(Needed.is_active).all()
    flash('Exporting list now, please wait...', 'info')
    msg = Message('--Shopping List--', sender=current_app.config['MAIL_USERNAME'],
                  recipients=current_app.config['MAIL_RECIPIENT'])
    with open('ideas.txt', 'a') as file:
        file.write('--Shopping List--\n\n')
        for item in items:
            file.write(str(item.data) + '\n')
            msg.body = str(item.data) + '\n'
            db.session.delete(item)
            db.session.commit()
        for need in needs:
            file.write(str(need.data) + '\n')
            msg.body = str(need.data) + '\n'
            db.session.delete(need)
            db.session.commit()
    system(f'/usr/bin/lpr {file}')
    mail.send(msg)
    flash('Export complete,', 'success')
    return redirect(url_for('supplies.supplies'))
