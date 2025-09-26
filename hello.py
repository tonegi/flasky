import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return f'<User {self.username}>'


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    message = None
    users = User.query.all()

    if form.validate_on_submit():
        name = form.name.data.strip()
        user = User.query.filter_by(username=name).first()

        if user is None:
            user = User(username=name)
            db.session.add(user)
            db.session.commit()
            message = "Prazer em conhecê-lo!"
        else:
            message = "Feliz em vê-lo novamente!"

        session['name'] = name
        return redirect(url_for('index'))

    return render_template('index.html', form=form, users=users, message=message, name=session.get('name'))


@app.context_processor
def inject_nav():
    return dict(home_url=url_for('index'))
