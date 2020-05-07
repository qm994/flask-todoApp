from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = '''postgresql://qingyuan:MAzhang199711#@127.0.0.1:5432/todoapp'''
db = SQLAlchemy(app)

# todo: what models do we need to control application? 
class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable = False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# create all tables 
db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.all()
    )