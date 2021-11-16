from flask import Blueprint, request, render_template, jsonify
from website.models import Chore
from website import db
from flask_login import current_user
from datetime import datetime as dt
import json

chores = Blueprint('chores', __name__)


@chores.route('/chore')
def chore():
    current_day = dt.today().weekday()
    if current_day < 5:
        chores_todo = Chore.query.filter_by(is_weekend=False)
    else:
        chores_todo = Chore.query.all()
    return render_template('chore.html', user=current_user, chores=chores_todo)


@chores.route('/delete-chore', methods=['POST'])
def delete_chore():
    task = json.loads(request.data)
    chore_id = task['choreId']
    task = task.query.get(chore_id)
    if task:
        if chore.user_id == current_user.id or current_user.is_parent:
            chore.is_active = False
            db.session.commit()

    return jsonify({})
