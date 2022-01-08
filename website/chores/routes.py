from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from website.chores.utils import chore_sorting
from website import db
from pathlib import Path
from website.models import Tasks
from flask_login import current_user
import json

chores = Blueprint('chores', __name__)


@chores.route('/chore')
def chore():
    if current_user.is_parent:
        tasks = Tasks.query.filter_by(is_approved=False)
    else:
        tasks = Tasks.query.filter_by(user_id=current_user.id, is_active=True)
    return render_template('chore.html', user=current_user, tasks=tasks)


@chores.route('/delete-chore', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    task_id = task['taskId']
    task = Tasks.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            task.is_active = False
            db.session.commit()
        elif current_user.is_parent and not task.is_active:
            task.is_approved = True
            db.session.commit()
    return jsonify({})


@chores.route('/get-chores')
def get_chores():
    database = str(Path(__file__).parent.parent) + '/database.db'
    chore_sorting(database)
    return redirect(url_for('chores.chore'))
