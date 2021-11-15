from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
Question

'''


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String(250), nullable=False)
    answer = Column(String(250), nullable=False)
    difficulty = Column(Integer, nullable=False)
    category_id = Column(Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='questions', lazy='joined', uselist=False)

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category.id,
            'difficulty': self.difficulty
        }


'''
Category

'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String(100), nullable=False)
    questions = db.relationship('Question', back_populates='category')

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
