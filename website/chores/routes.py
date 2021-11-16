from flask import Blueprint, request, flash, render_template, jsonify
from website.models import Chore, Tasks
from website import db
from flask_login import current_user
from datetime import datetime as dt
import json

chores = Blueprint('chores', __name__)


@chores.route('/chore')
def chore():
    current_day = dt.today().weekday()
    # chore_split = []
    if current_day < 5:
        chores_todo = Chore.query.filter_by(is_weekend=False)
    else:
        chores_todo = Chore.query.all()
    # for iteration, row in enumerate(chores_todo):
    #     chore_split.append(row)
    #     if iteration <= int(len(chore_split) / 2):
    #         new_task = Tasks(task=chore_split, user_id=2)
    #     else:
    #         new_task = Tasks(task=chore_split, user_id=3)
    # db.session.add(new_task)
    # db.session.commit()
    # tasks = Tasks.query.filter_by(is_active=True)
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
