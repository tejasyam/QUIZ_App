from app.models import *
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from app.schemas import *
from app.services import *
from app import api, docs


class SignUpAPI(MethodResource, Resource):
    @doc(description='Sign Up API', tags=['SignUp API'])
    @use_kwargs(SignUpRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            create_user(**kwargs)
            return APIResponse().dump(dict(message='User is successfully registered')), 201
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to Register User : {str(e)}')), 400


class LoginAPI(MethodResource, Resource):
    @doc(description='Login API', tags=['Login API'])
    @use_kwargs(LoginRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            is_logged_in, session_id, user_id = login_user(**kwargs)

            if is_logged_in:
                return APIResponse().dump(
                    dict(
                        message='User is successfully logged in',
                        session_id=session_id,
                        user_id=user_id
                    )
                ), 200

            return APIResponse().dump(dict(message='User not found')), 404

        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to login User: {str(e)}')), 400


class LogoutAPI(MethodResource, Resource):
    @doc(description='Logout API', tags=['Logout API'])
    @use_kwargs(LogoutRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            is_logged_out = logout_user(kwargs['session_id'])

            if is_logged_out:
                return APIResponse().dump(dict(message='User is successfully logged out')), 200

            return APIResponse().dump(dict(message='User is not logged in')), 401

        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to logout User: {str(e)}')), 400


class ListQuestionAPI(MethodResource, Resource):
    @doc(description='List Questions API', tags=['Questions'])
    @use_kwargs(QuestionsRequest, location='json')
    @marshal_with(ListQuestionsResponse)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id'])

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_if_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not admin user')), 401

            questions_list = QuestionMaster.query.all()
            questions = []

            for i in questions_list:
                questions.append({
                    'id': i.id,
                    'question': i.question,
                    'choice1': i.choice1,
                    'choice2': i.choice2,
                    'choice3': i.choice3,
                    'choice4': i.choice4,
                    'answer': i.answer,
                    'marks': i.marks
                })

            return ListQuestionsResponse().dump(dict(questions=questions)), 200

        except Exception as e:
            return APIResponse().dump(dict(message=f'Error in listing questions : {str(e)}')), 400


class AddQuestionAPI(MethodResource, Resource):
    @doc(description='Add Question API', tags=['Questions'])
    @use_kwargs(AddQuestionRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id'])

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_if_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not admin user')), 401

            add_question(**kwargs)
            return APIResponse().dump(dict(message='Question is successfully added')), 200

        except Exception as e:
            return APIResponse().dump(dict(message=f'Error in adding question : {str(e)}')), 400


class CreateQuizAPI(MethodResource, Resource):
    @doc(description='Create Quiz API', tags=['Quiz'])
    @use_kwargs(CreateQuizRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id'])

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_if_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not the admin user')), 401

            create_quiz(**kwargs)
            return APIResponse().dump(dict(message='Quiz is successfully created')), 200

        except Exception as e:
            return APIResponse().dump(dict(message=f'Error in creating quiz : {str(e)}')), 400


class AssignQuizAPI(MethodResource, Resource):
    @doc(description='Assign Quiz API', tags=['Quiz'])
    @use_kwargs(AssignQuizRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id'])

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_if_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not the admin user')), 401

            assign_quiz(**kwargs)
            return APIResponse().dump(dict(message='Quiz assigned successfully')), 200

        except Exception as e:
            return APIResponse().dump(dict(message=f'Error in assigning quiz : {str(e)}')), 400


class ViewQuizAPI(MethodResource, Resource):
    @doc(description='View Quiz API', tags=['Quiz'])
    @use_kwargs(ViewQuizRequest, location='json')
    @marshal_with(ViewQuiz)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id'])

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_if_admin(user_id)

            check_access = QuizInstance.query.filter_by(
                quiz_id=kwargs['quiz_id'],
                user_id=user_id
            ).first()

            if not check_access and not is_admin:
                return APIResponse().dump(
                    dict(message='Quiz is not assigned to user')
                ), 401

            quiz_question_ids = QuizQuestions.query.filter_by(
                quiz_id=kwargs['quiz_id']
            ).all()

            question_ids = []

            for i in quiz_question_ids:
                question_ids.append(i.question_id)

            questions_all = QuestionMaster.query.filter(
                QuestionMaster.id.in_(question_ids)
            ).all()

            questions_output = []

            for i in questions_all:
                questions_output.append({
                    'Question': i.question,
                    'choices': [i.choice1, i.choice2, i.choice3, i.choice4]
                })

            return ViewQuiz().dump(dict(quiz_questions=questions_output)), 200

        except Exception as e:
            return APIResponse().dump(dict(message=f'Error in viewing quiz : {str(e)}')), 400


class ViewAssignedQuizAPI(MethodResource, Resource):
    @doc(description='View Assigned Quiz API', tags=['Quiz'])
    @use_kwargs(AssignedQuizRequest, location='json')
    @marshal_with(ListQuizs)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id'])

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            quiz = QuizInstance.query.filter_by(user_id=user_id).all()
            quizs = []

            for i in quiz:
                quizs.append({
                    'quiz_id': i.quiz_id,
                    'is_submitted': i.is_submitted,
                    'score_acheived': getattr(i, 'score_acheived', getattr(i, 'score', 0))
                })

            return ListQuizs().dump(dict(quizs=quizs)), 200

        except Exception as e:
            return APIResponse().dump(dict(message=f'Error in viewing assigned quizzes : {str(e)}')), 400


class ViewAllQuizAPI(MethodResource, Resource):
    @doc(description='View All Quiz API', tags=['Quiz'])
    @use_kwargs(ViewAllQuizRequest, location='json')
    @marshal_with(ListViewAllQuiz)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id'])

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_if_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not the admin user')), 401

            quizs_list = QuizMaster.query.all()
            quiz_list = []

            for i in quizs_list:
                quiz_list.append({
                    'Quiz_id': i.id,
                    'Quiz_name': i.quiz_name
                })

            return ListViewAllQuiz().dump(dict(quizs=quiz_list)), 200

        except Exception as e:
            return APIResponse().dump(dict(message=f'Error in viewing all quizzes : {str(e)}')), 400


api.add_resource(SignUpAPI, '/signup')
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(ListQuestionAPI, '/list.questions')
api.add_resource(AddQuestionAPI, '/add.question')
api.add_resource(CreateQuizAPI, '/create.quiz')
api.add_resource(AssignQuizAPI, '/assign.quiz')
api.add_resource(ViewQuizAPI, '/view.quiz')
api.add_resource(ViewAssignedQuizAPI, '/assigned.quizzes')
api.add_resource(ViewAllQuizAPI, '/all.quizzes')

docs.register(SignUpAPI)
docs.register(LoginAPI)
docs.register(LogoutAPI)
docs.register(ListQuestionAPI)
docs.register(AddQuestionAPI)
docs.register(CreateQuizAPI)
docs.register(AssignQuizAPI)
docs.register(ViewQuizAPI)
docs.register(ViewAssignedQuizAPI)
docs.register(ViewAllQuizAPI)