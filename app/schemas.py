from email.policy import default
from marshmallow import Schema, fields, base

class APIResponse(Schema):
    message = fields.Str()
    session_id = fields.Str()
    user_id = fields.Int()
    quiz_id = fields.Int()
    score = fields.Int()


class SignUpRequest(Schema):
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    is_admin = fields.Int(required=True)


class LoginRequest(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class LogoutRequest(Schema):
    session_id = fields.Str(required=True)

class QuestionsRequest(Schema):
    session_id=fields.Str(default="session_id")

class ListQuestionsResponse(Schema):
    questions=fields.List(fields.Dict())

class AddQuestionRequest(Schema):
    session_id = fields.Str(required=True)

    question = fields.Str(required=True)

    choice1 = fields.Str(required=True)
    choice2 = fields.Str(required=True)
    choice3 = fields.Str(required=True)
    choice4 = fields.Str(required=True)

    answer = fields.Int(required=True)
    marks = fields.Int(required=True)

    remarks = fields.Str(required=True)

class CreateQuizRequest(Schema):
    session_id= fields.Str(default="session_id")
    quiz_name=fields.Str(default="quiz_id")
    question_ids=fields.List(fields.String)

class AssignQuizRequest(Schema):
    session_id = fields.Str(required=True)
    quiz_id = fields.Int(required=True)
    user_id = fields.Int(required=True)

class ViewQuizRequest(Schema):
    session_id=fields.Str(default="session_id")
    quiz_id=fields.Str(default="quiz_id")

class AssignedQuizRequest(Schema):
    session_id=fields.Str(default="session_id")

class ListQuizs(Schema):
    quizs=fields.List(fields.Dict())

class ViewAllQuizRequest(Schema):
    session_id=fields.Str(default="session_id")

class ListViewAllQuiz(Schema):
    quizs=fields.List(fields.Dict())

class ViewQuiz(Schema):
    quiz_questions=fields.List(fields.Dict())