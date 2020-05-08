from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy, SessionBase
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' % self.id

class Done(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_finished = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Done %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST' and request.form['content']!= "":
    task_content = request.form['content']
    new_task = Todo(content=task_content)

    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return 'Tere was an error while adding the task'

  elif request.method == 'POST' and request.form['content']== "":
    return print("erro")

  else:
      tasks = Todo.query.order_by(Todo.date_created).all()
      tasks_done = Done.query.order_by(Done.date_finished).all()
      return render_template('index.html', tasks=tasks, tasks_done=tasks_done)

@app.route('/complete/<int:id>')
def complete(id):
  task_to_complete = Todo.query.get_or_404(id)
  task_content = task_to_complete.content
  complete_task = Done(content=task_content)

  try:
    db.session.add(complete_task)
    db.session.delete(task_to_complete)
    db.session.commit()
    return redirect('/')
  except:
    return 'The task could not be completed, please try again'

@app.route('/clear')
def clear():
  
  db.session.query(Done).delete()
  db.session.commit()
  return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)

  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was an error deleting the task'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  task = Todo.query.get_or_404(id)

  if request.method == 'POST':
    task.content = request.form['content']
    
    try:
      db.session.commit()
      return redirect('/')
    except:
      return "There was an error editing the task"

  else:
    return render_template('edit.html', task=task)

if __name__ == "__main__":
  app.run(debug=True)
  db.create_all()