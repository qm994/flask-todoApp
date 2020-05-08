from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = '''postgresql://qingyuan:MAzhang199711#@127.0.0.1:5432/todoapp'''
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# todo: what models do we need to control application?


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # description = request.form.get("description", "")
        description = request.get_json()['description']
        # next use the new desciption to insert to db
        # 1. make it associate to db and add to pending changes
        todo = Todo(description=description)
        db.session.add(todo)
        # 2. commit to db
        db.session.commit()
        body['description'] = todo.description 
    except:
        error = True 
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else: 
        # 3. controller show what view to the user after we make commit:
    # redirect to index home route so it shows all newly data
    # return redirect(url_for("index"))
        return jsonify(body)

# by includes in `<>` , we can use it later
# @app.route('/todos/<todo_id>/set-completed', methods=['POST'])
# def set_completed_todo(todo_id):
#     try:
#         completed = requested.get_json()['completed']
#         print('completed', completed)
#         todo = Todo.query.get(todo_id)
#         todo.completed = completed
#         db.session.commit()
#     except:
#         db.session.rollback()
#     finally:
#         db.session.close()
#     #return redirect(url_for("index"))
#     return "hello"

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all())