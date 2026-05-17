import uuid
from app.models import *
from app.models import db


def create_user(**kwargs):
    user = UserMaster(
        name=kwargs['name'],
        username=kwargs['username'],
        password=kwargs['password'],
        is_admin=kwargs['is_admin']
    )

    db.session.add(user)
    db.session.commit()


def login_user(**kwargs):
    user = UserMaster.query.filter_by(
        username=kwargs['username'],
        password=kwargs['password']
    ).first()

    if not user:
        return False, None, None

    session_id = str(uuid.uuid4())

    session = UserSession(
        user_id=user.id,
        session_id=session_id,
        is_active=1
    )

    db.session.add(session)
    db.session.commit()

    return True, session_id, user.id


def logout_user(session_id):
    session = UserSession.query.filter_by(
        session_id=session_id,
        is_active=1
    ).first()

    if not session:
        return False

    session.is_active = 0
    db.session.commit()

    return True


def check_user_session_is_active(session_id):
    session = UserSession.query.filter_by(
        session_id=session_id,
        is_active=1
    ).first()

    if not session:
        return False, None

    return True, session.user_id


def check_if_admin(user_id):
    user = UserMaster.query.filter_by(id=user_id).first()

    if user and user.is_admin == 1:
        return True

    return False


def add_question(**kwargs):
    question = QuestionMaster(
        question=kwargs['question'],
        choice1=kwargs['choice1'],
        choice2=kwargs['choice2'],
        choice3=kwargs['choice3'],
        choice4=kwargs['choice4'],
        answer=kwargs['answer'],
        marks=kwargs['marks'],
        remarks=kwargs['remarks']
    )

    db.session.add(question)
    db.session.commit()

def create_quiz(**kwargs):
    quiz = QuizMaster(
        quiz_name=kwargs['quiz_name']
    )

    db.session.add(quiz)
    db.session.commit()

    return quiz.id

def assign_quiz(**kwargs):
    quiz_instance = QuizInstance(
        quiz_id=kwargs['quiz_id'],
        user_id=kwargs['user_id'],
        score=0,
        is_submitted=0
    )

    db.session.add(quiz_instance)
    db.session.commit()

    return True