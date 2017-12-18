from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm,Language_Support_dict
from flask import Flask, session, redirect, url_for, escape, request

@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        session['my_language'] = form.my_language.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
        form.my_language.data = session.get('my_language', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    my_language = session.get('my_language','')
    my_language_fullname = Language_Support_dict.get(my_language)
    print(session)
    if name == '' or room == '' or my_language=='':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, my_language=my_language,my_language_fullname = my_language_fullname)

