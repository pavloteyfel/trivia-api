from flask import Flask, request, abort, jsonify
from models import db, Question, Category
from flask_cors import CORS

import random

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/')
    def index():
        return jsonify({}), 200

    @app.route('/api/v1.0/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)

        # Throws 404 by default if there is non existing page
        pages = Question.query.order_by(Question.id).paginate(page, QUESTIONS_PER_PAGE)
        categories = Category.query.all()

        # Abort if there are no entries
        if not categories:
            abort(404)

        # Format the categories
        categories_formatted = {}
        for category in categories:
            categories_formatted[category.id] = category.type

        return jsonify({
            'questions': [question.format() for question in pages.items],
            'totalQuestions': pages.total,
            'categories': categories_formatted,
            'currentCategory': None,
        }), 200

    @app.route('/api/v1.0/categories/<int:id>/questions', methods=['GET'])
    def get_questions_of_category(id):
        # Throws 404 if not found or bad id provided
        category = Category.query.get_or_404(id)

        questions = Question.query.filter(Question.category_id == id).all()

        # Abort if there are no questions found
        if not questions:
            abort(404)

        return jsonify({
            'questions': [question.format() for question in questions],
            'totalQuestions': len(questions),
            'currentCategory': category.type,
        }), 200

    @app.route('/api/v1.0/categories', methods=['GET'])
    def get_categories():
        categories_formatted = {}
        categories = Category.query.all()

        # Abort if there are no entries
        if not categories:
            abort(404)

        # Puts all the categories specific format for the frontend
        for category in categories:
            categories_formatted[category.id] = category.type

        return jsonify({'categories': categories_formatted}), 200

    @app.route('/api/v1.0/questions/<int:id>', methods=['DELETE'])
    def delete_questions(id):

        # Throws 404 if there is no question found or bad id provided
        question = Question.query.get_or_404(id)

        try:
            db.session.delete(question)
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
        return jsonify({}), 202

    @app.route('/api/v1.0/questions', methods=['POST'])
    def create_questions():
        """Creates a question or searches for one"""
        request_data = request.get_json()

        # if there is a search term, then we let's find something
        if request_data.get('searchTerm'):
            search_term = request_data.get('searchTerm')
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            # abort the operation if are 0 result, current front end doesn't like it
            if not questions:
                abort(404)

            return jsonify({
                'questions': [question.format() for question in questions],
                'totalQuestions': len(questions),
                'currentCategory': None,
            }), 200

        # then the request is about new question creation, 
        # if acquiring of the attributes fails we abort the operation with 400
        try:
            category_id = request_data['category']
            question = request_data['question']
            answer = request_data['answer']
            difficulty = request_data['difficulty']
        except KeyError:
            abort(400)

        category = Category.query.get_or_404(category_id)

        try:
            question_obj = Question(question=question, answer=answer,
                                    difficulty=difficulty, category=category)
            db.session.add(question_obj)
            db.session.commit()
        # if there is problem with db we abort with 422
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

        return jsonify({}), 201

    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def get_quizzes():
        request_data = request.get_json()

        # validate the content of the request, in case of error: 422
        try:
            previous_ids = request_data['previous_questions']
            category_data = request_data['quiz_category']
            category_id = int(category_data['id'])
        except KeyError:
            abort(400)

        # get a question from a specific category that was not already used
        if category_id > 0:
            category = Category.query.get_or_404(category_id)
            filtered_questions = [question for question in category.questions if question.id not in previous_ids]

        # get a question from any category that was not already used
        else:
            questions = Question.query.filter(Question.id.notin_(previous_ids))
            filtered_questions = [question for question in questions]

        # if there are questions remained then choose randomly one
        if filtered_questions:
            return jsonify({
                'question': random.choice(filtered_questions).format()
            }), 201

        # if there is no questions left, send null
        else:
            return jsonify({
                'question': None
            }), 201

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": 400, "message": "bad request"}), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({"error": 404, "message": "resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": 405, "message": "method not allowed"}), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({"error": 422, "message": "unprocessable entity"}), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": 500, "message": "internal server error"}), 500

    return app
