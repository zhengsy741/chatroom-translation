from flask import session, g
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from google.cloud import translate
import six
import os
from oauth2client.client import GoogleCredentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./google_secret_keys.json"
print(os.environ)

translate_client = translate.Client()

credentials = GoogleCredentials.get_application_default()

@socketio.on('joined room', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    my_language = session.get('my_language')
    target_language = my_language
    # target_language = session.get('language')
    # print(str(my_language)+" | "+str(target_language))
    msg_orig =' has entered the room.'
    msg_translated = translate_client.translate(
        str(msg_orig),source_language='en',
        target_language=target_language)
    # msg_joined = session.get('name') + " " +
    # g.current_user = User(name=session.get('name'),room=session.get('room'),my_language=my_language)
    # emit('join message', {'sender_name': session.get('name') ,"msg_orig": msg_orig},room=room)
    emit('join message', {'sender_name': session.get('name') ,"translated_msg": msg_translated['translatedText']},room=room)

@socketio.on("join message to others",namespace="/chat")
def join_message_to_others(message):
    my_language = session.get('my_language')
    room = session.get('room')
    msg_translated = translate_client.translate(
        str(message['translated_msg']),
        target_language=my_language)
    emit('send join message to others', {'username': message['sender_name'],"translated_msg": msg_translated['translatedText']})

@socketio.on('read text', namespace='/chat')
def read_text(message):
    text = message['msg']
    target = _detect_language(text)

@socketio.on('sendMessage',namespace='/chat')
def send_message(message):
    name=session.get('name')
    room=session.get('room')
    emit('receiveMessage', {'sender_name': name,'message':message},room=room)


@socketio.on('left room', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    my_language = session.get('my_language')
    target_language = my_language
    msg_left =' has left the room.'
    msg_left = session.get('name') + " " +msg_left
    g.current_user = User(name=session.get('name'),room=session.get('room'),my_language=my_language)
    emit('left message', {'username': session.get('name') ,"translated_msg": msg_left}, room=room)

@socketio.on('all users',namespace='/chat')
def get_user_list(message):
    print(message)

@socketio.on('translate message',namespace='/chat')
def translate_message(message):
    target_language = session.get('my_language')
    orig_message = message['message']
    translate_msg = translate_client.translate(str(orig_message),target_language=target_language)
    message["translated_msg"]=translate_msg['translatedText']
    emit("sendback translated message",{"message":message})



def _detect_language(text):
    target_language = translate_client.detect_language(text)
    return target_language

class User(object):
    def __init__(self,name=None,room=None,my_language=None,target_language=None):
        self.name=name
        self.room=room
        self.my_language = my_language
        self.target_language=target_language
