from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from datetime import datetime, timezone
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

bootstrap = Bootstrap(app)
moment = Moment(app)

class Form(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if 'utoronto' not in field.data:
            raise ValidationError('Email must be a University of Toronto address.')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        flash('Form submitted successfully!')
        return redirect(url_for('index'))
    
    return render_template('user.html',
                           form=form,
                           name=session.get('name'), 
                           email=session.get('email'),
                           current_time=datetime.now(timezone.utc))

@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    form = Form()
    
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        flash('Form submitted successfully!')
        return redirect(url_for('index'))
    
    return render_template('user.html', 
                           form=form,
                           name=session.get('name'), 
                           email=session.get('email'),
                           current_time=datetime.now(timezone.utc))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500