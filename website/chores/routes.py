from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from website.chores.utils import chore_sorting
from datetime import datetime as dt
from website import db
from website.models import Tasks
from flask_login import current_user
import json
from pathlib import Path

chores = Blueprint('chores', __name__)


@chores.route('/chore')
def chore():
    if current_user.is_parent:
        tasks = Tasks.query.filter_by(is_approved=False)
    else:
        tasks = Tasks.query.filter_by(user_id=current_user.id, is_active=True)
    return render_template('chore.html', user=current_user, tasks=tasks)


@chores.route('/delete-chore', methods=['POST'])
def delete_taske():
    task = json.loads(request.data)
    task_id = task['taskId']
    task = Tasks.query.get(task_id)
    if task:
        if task.user_id == current_user.id or current_user.is_parent:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})


@chores.route('/approve-chore', methods=['POST'])
def approve_chore():
    task = json.loads(request.data)
    task_id = task['taskId']
    task = Tasks.query.get(task_id)
    if task:
        if chore.user_id == current_user.id or current_user.is_parent:
            chore.is_approved = True
            db.session.commit()
    return jsonify({})


@chores.route('/reject-chore', methods=['POST'])
def reject_chore():
    task = json.loads(request.data)
    task_id = task['taskId']
    task = Tasks.query.get(task_id)
    if task:
        if chore.user_id == current_user.id or current_user.is_parent:
            chore.is_active = True
            db.session.commit()
    return jsonify({})


@chores.route('/get-chores')
def get_chores():
    database = str(Path(__file__).parent) + '/../database.db'
    chore_sorting(database)
    return redirect(url_for('chores.chore'))
