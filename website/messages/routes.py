from flask import Blueprint, flash, redirect, url_for, render_template
from website.messages.forms import MessageForm
from website import db
from website.models import Message, User
from flask_login import current_user, login_required

messages = Blueprint('messages', __name__)


@messages.route('/message', methods=['GET', 'POST'])
@login_required
def message():
    msgs = Message.query.all()
    return render_template('messages.html', title='Messages', user=current_user.first_name, messages=msgs, )


@messages.route("/new_message", methods=['GET', 'POST'])
@login_required
def new_message():
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender=form.sender.data, recipient=form.recipient.data.id, message=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('messages.message'))
    return render_template('create_msg.html', title='New Message',
                           form=form, legend='New Message')


