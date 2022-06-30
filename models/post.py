from datetime import datetime

from models.settings import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # database relationship
    author = db.relationship("User")  # orm relationship
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(self, title, description, author):
        newPost = self(title=title, description=description, author=author)
        db.add(newPost)
        db.commit()
        return newPost
