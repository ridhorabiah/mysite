from datetime import datetime
from mysite import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


usages = db.Table(
    'usages',
    db.Column('wu_id', db.Integer, db.ForeignKey('work_unit.id'), nullable=False),
    db.Column('app_id', db.Integer, db.ForeignKey('application.id'), nullable=False)
    )


class WorkUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    employees = db.relationship('Employee', backref='unit', lazy=True)
    apps = db.relationship('Application', secondary=usages,
                           backref=db.backref('work_units', lazy='dynamic'),
                           lazy='dynamic')

    def __repr__(self):
        return self.name


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    nip = db.Column(db.String(18), unique=True)
    wu_id = db.Column(db.Integer, db.ForeignKey('work_unit.id'), nullable=False)
    account = db.relationship('User', uselist=False, backref='owned')

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))  # set unique
    apps_post = db.relationship('Application', backref='posted_by', lazy=True)

    def __repr__(self):
        return self.username


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    platform = db.Column(db.String(30), nullable=False)
    database = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return self.name
