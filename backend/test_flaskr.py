from flask_migrate import Migrate, upgrade, downgrade
from models import Question, Category, db
from flask_testing import TestCase
from flaskr import create_app

import unittest
import logging


# Turning off migration related logging INFO
logging.getLogger('alembic.runtime.migration').disabled = True

class TriviaTestCase(TestCase):
    """This class represents the trivia test case"""

    DB_PATH = 'postgresql://postgres:postgres@localhost:5432/trivia_test'

    def create_app(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = self.DB_PATH
        Migrate(app, db)
        return app

    def setUp(self):
        """Prepares the app for testing:
            - Creates tables
            - Clears session
            - Populates the database with seed data
        """
        upgrade()
        db.session.commit()

    def tearDown(self):
        """
        Executed after reach test:
            - Closes all sessions
            - Drops all tables stored in this metadata
        """
        db.session.remove()
        downgrade()

    def test_get_categories(self):
        """
        Checks:
            - status_code == 200
            - presence of "categories" attribute
        """
        response = self.client.get('/api/v1.0/categories')
        self.assertTrue(response.status_code == 200)
        data = response.get_json()
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        """
        Checks:
            - status_code == 200
            - 10 items per page
            - total amount of questions
            - presence of the required attributes (4)
        """
        response = self.client.get('/api/v1.0/questions')
        self.assertTrue(response.status_code == 200)
        data = response.get_json()
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) == 10)
        self.assertTrue(data['totalQuestions'] == 19)
        self.assertTrue(data['categories'])
        self.assertFalse(data['currentCategory'])

    def test_search_questions(self):
        """
        Checks:
            - status_code == 200
            - presence of the required attributes (4)
            - the searched question was returned based on the search criteria
        """
        body = {'searchTerm': 'taj mahal'}
        response = self.client.post('/api/v1.0/questions', json=body)
        self.assertTrue(response.status_code == 200)
        data = response.get_json()
        self.assertTrue(data['questions'])
        self.assertTrue(data['questions'][0]['question'])
        self.assertTrue(data['questions'][0]['answer'])
        self.assertTrue(data['questions'][0]['difficulty'])
        self.assertTrue(data['questions'][0]['id'])
        self.assertTrue(data['questions'][0]['id'] == 11)

    def test_get_questions_of_category(self):
        """
        Checks:
            - status_code == 200
            - presence of the required attributes (3)
            - correct amount of total questions
            - correctness of the category type
        """
        category_obj = Category.query.get(1)
        response = self.client.get('/api/v1.0/categories/1/questions')
        self.assertTrue(response.status_code == 200)
        data = response.get_json()
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])
        self.assertTrue(len(data['questions']) == len(category_obj.questions))
        self.assertTrue(data['totalQuestions'] == len(category_obj.questions))
        self.assertTrue(data['currentCategory'] == category_obj.type)

    def test_delete_questions(self):
        """
        Checks:
            - status_code == 202
            - if the delete request was accepted and removed from database
            - if empty response was received
        """
        response = self.client.delete('/api/v1.0/questions/18')
        self.assertTrue(response.status_code == 202)
        data = response.get_json()
        question = Question.query.get(18)
        self.assertFalse(question)
        self.assertFalse(data)

    def test_create_questions(self):
        """
        Checks:
            - status_code == 201
            - if the post request was acceped and insrted into the db
            - if empty response was received
        """
        body = {
            'question': 'Sample question',
            'answer': 'Sample anwser',
            'difficulty': '1',
            'category': 1
        }
        response = self.client.post('/api/v1.0/questions', json=body)
        self.assertTrue(response.status_code == 201)
        data = response.get_json()
        question = Question.query.filter_by(question='Sample question').first()
        self.assertTrue(question)
        self.assertFalse(data)

    def test_get_quizzes(self):
        """
        Checks:
            - status_code == 201
            - if the post request was acceped and proper question of
            a category was returned(Category.id > 0)
            - if questions are omitted by the "previous_questions" attribute
        """
        category = Category.query.get(1)
        questions_ids = [question.id for question in category.questions]
        remaining_question = questions_ids.pop()
        body = {
            'previous_questions': questions_ids,
            'quiz_category': {
                'type': category.type,
                'id': category.id
            }
        }
        response = self.client.post('/api/v1.0/quizzes', json=body)
        self.assertTrue(response.status_code == 201)
        data = response.get_json()
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['id'] == remaining_question)
        self.assertTrue(data['question']['category'] == category.id)

    def test_get_quizzes_all_category(self):
        """
        Checks:
            - status_code == 201
            - if the post request was accepted and a question was returned of
            any category (Category.id == 0)
            - if questions are omitted by the "previous_questions" attribute
        """
        questions = Question.query.all()
        questions_ids = [question.id for question in questions]
        remaining_question = questions_ids.pop()
        body = {
            'previous_questions': questions_ids,
            'quiz_category': {
                'type': '',
                'id': 0
            }
        }
        response = self.client.post('/api/v1.0/quizzes', json=body)
        self.assertTrue(response.status_code == 201)
        data = response.get_json()
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['id'] == remaining_question)

    def test_resoure_not_found_404(self):
        """
        Checks:
            - status code 404 and message error in case of non existent
            endpoint call
        """
        response = self.client.get('/api/v1.0/play')
        self.assertTrue(response.status_code == 404)
        data = response.get_json()
        self.assertTrue(data['message'] == 'resource not found')

    def test_delete_questions_404(self):
        """
        Checks:
            - status code 404 and message error in case of non existent
            question id
        """
        response = self.client.delete('/api/v1.0/questions/9999')
        self.assertTrue(response.status_code == 404)
        data = response.get_json()
        self.assertTrue(data['message'] == 'resource not found')

    def test_create_questions_400(self):
        """
        Checks:
            - status code 400 and message error in case of missing attributes
        """
        body = {
            'questions': 'Sample question'
        }
        response = self.client.post('/api/v1.0/questions', json=body)
        self.assertTrue(response.status_code == 400)
        data = response.get_json()
        self.assertTrue(data['error'] == 400)

    def test_get_quizzes_400(self):
        """
        Checks:
            - status code 400 and message error in case of missing attributes
        """

        body = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'click'
            }
        }
        response = self.client.post('/api/v1.0/quizzes', json=body)
        response
        self.assertTrue(response.status_code == 400)
        data = response.get_json()
        self.assertTrue(data['error'] == 400)

    def test_get_quizzes_404(self):
        """
        Checks:
            - status code 404 and message error in case of missing attributes
        """
        body = {
            'previous_questions': [],
            'quiz_category': {
                'type': '',
                'id': 99999
            }
        }
        response = self.client.post('/api/v1.0/quizzes', json=body)
        self.assertTrue(response.status_code == 404)
        data = response.get_json()
        self.assertTrue(data['message'] == 'resource not found')

    def test_method_not_allowed_405(self):
        """
        Checks:
            - status code 405 and message error in case of bad method request
        """
        response = self.client.put('/api/v1.0/questions', json={})
        self.assertTrue(response.status_code == 405)
        data = response.get_json()
        self.assertTrue(data['message'] == 'method not allowed')


if __name__ == "__main__":
    unittest.main()
