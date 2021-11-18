from flask import Blueprint, request, render_template, jsonify
from website.chores.utils import chore_sorting
from website import db
from datetime import datetime as dt
from website.models import Tasks
from flask_login import current_user
import json
from pathlib import Path

chores = Blueprint('chores', __name__)


@chores.route('/chore')
def chore():
    database = str(Path(__file__).parent) + '/../database.db'
    current_date = dt.now().strftime('%Y-%m-%d')
    if Tasks.query.filter(Tasks.date >= current_date):
        if current_user.is_parent:
            tasks = Tasks.query.filter_by(is_active=True)
        else:
            tasks = Tasks.query.filter_by(user_id=current_user.id, is_active=True)
    else:
        if current_user.is_parent:
            tasks = Tasks.query.filter_by(is_active=True)
        else:
            chore_sorting(database)
            tasks = Tasks.query.filter_by(user_id=current_user.id, is_active=True)
    return render_template('chore.html', user=current_user, chores=tasks)


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
