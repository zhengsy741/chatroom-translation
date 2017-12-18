from flask_wtf import Form
from flask import g,app

from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import Required



Language_Support= [('hy','Armenian'),('zh','Chinese'),('cs','Czech'),('da','Danish'),('nl','Dutch'),('en','English'),
                   ('eo','Esperanto'),('fi','Finnish'),('fr','French'),('ka','Georgian'),('de','German'),('el','Greek'),
                   ('it','Italian'),('ja','Japanese'),('ko','Korean'),('ku','Kurdish'),('fa','Persian'),('pl','Polish'),
                   ('pt','Portuguese'),('ro','Romanian'),('ru','Russian'),('es','Spanish'),('sv','Swedish'),
                   ('tr','Turkish'),('ur','Urdu')]
Language_Support_dict= {'hy':'Armenian','zh':'Chinese','cs':'Czech','da':'Danish','nl':'Dutch','en':'English',
                   'eo':'Esperanto','fi':'Finnish','fr':'French','ka':'Georgian','de':'German','el':'Greek',
                   'it':'Italian','ja':'Japanese','ko':'Korean','ku':'Kurdish','fa':'Persian','pl':'Polish',
                   'pt':'Portuguese','ro':'Romanian','ru':'Russian','es':'Spanish','sv':'Swedish',
                   'tr':'Turkish','ur':'Urdu'}
class LoginForm(Form):
    """Accepts a nickname and a room.Select a target language"""

    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    my_language = SelectField('Language',choices=Language_Support, validators=[Required()])
    submit = SubmitField('Enter Chatroom')

