from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import application

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(application)


class UserMaster(db.Model):
    __tablename__ = 'user_master'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Integer, default=1)
    created_ts = db.Column(db.DateTime, default=datetime.utcnow)


class UserSession(db.Model):
    __tablename__ = 'user_session'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_master.id'))
    session_id = db.Column(db.String(200), unique=True)
    is_active = db.Column(db.Integer, default=1)
    created_ts = db.Column(db.DateTime, default=datetime.utcnow)


class QuestionMaster(db.Model):
    __tablename__ = 'question_master'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), unique=True)
    choice1 = db.Column(db.String(500))
    choice2 = db.Column(db.String(500))
    choice3 = db.Column(db.String(500))
    choice4 = db.Column(db.String(500))
    answer = db.Column(db.Integer)
    marks = db.Column(db.Integer)
    remarks = db.Column(db.String(200))


class QuizMaster(db.Model):
    __tablename__ = 'quiz_master'

    id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(200), unique=True)


class QuizQuestions(db.Model):
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz_master.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question_master.id'))


class QuizInstance(db.Model):
    __tablename__ = 'quiz_instance'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz_master.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_master.id'))
    score = db.Column(db.Integer, default=0)
    is_submitted = db.Column(db.Integer, default=0)


class UserResponses(db.Model):
    __tablename__ = 'user_responses'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    response = db.Column(db.Integer)