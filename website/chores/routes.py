from flask import Blueprint, request, render_template, jsonify
from website.chores.utils import chore_sorting
from website import db
from flask_login import current_user
import json
from pathlib import Path

chores = Blueprint('chores', __name__)


@chores.route('/chore')
def chore():
    all_chores = []
    database = str(Path(__file__).parent) + '/database.db'
    chores_todo = chore_sorting(database)
    if current_user.id == 2:
        tasks = chores_todo[1]
    elif current_user.id == 3:
        tasks = chores_todo[0]
    else:
        all_chores.append(chores_todo[0])
        all_chores.append(chores_todo[1])
        tasks = all_chores
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
