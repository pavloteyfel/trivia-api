from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Question(db.Model):
    """Table structure for question data"""
    
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String(250), nullable=False)
    answer = Column(String(250), nullable=False)
    difficulty = Column(Integer, nullable=False)
    category_id = Column(Integer, db.ForeignKey('categories.id'),
                         nullable=False)
    category = db.relationship('Category', back_populates='questions',
                               lazy='joined', uselist=False)

    def format(self):
        """Helper function for preparing model data in proper form"""

        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category.id,
            'difficulty': self.difficulty
        }


class Category(db.Model):
    """Table scruture for category types"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String(100), nullable=False)
    questions = db.relationship('Question', back_populates='category')

    def format(self):
        """Helper function for preparing model data in proper form"""
        return {
            'id': self.id,
            'type': self.type
        }
