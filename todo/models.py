from todo import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)
    lists = db.relationship('List', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    def __repr__(self):
        return '<Todo %r>' % self.item

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.name

