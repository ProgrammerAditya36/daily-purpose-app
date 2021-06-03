from flask import Flask, redirect, render_template,request
from newsapi import NewsApiClient
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
import datetime
today = datetime.datetime.now().strftime("%d/%m/%Y")
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
class Diary(db.Model):
    s_no = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(200), nullable=False)
    des = db.Column(db.String(65000), nullable=False)
    date_created =db.Column(db.String(30), default=today)
    def __repr__(self) -> str:
        return f"{self.s_no} - {self._title}"
@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/todolist', methods = ['GET', 'POST'])
def result():
    if request.method == 'POST':
      result = request.form
      title = result['title']
      description = result['desc']
      add_todo = Todo(title=title, desc=description)
      db.session.add(add_todo)
      db.session.commit()
    allTodo = Todo.query.all()
    return render_template("todolist.html",allTodo = allTodo)

@app.route('/diary', methods = ['GET', 'POST'])
def diary():
    if request.method == 'POST':
      result = request.form
      title = result['_title']
      description = result['des']
      add_diary = Diary(_title=title, des=description)
      db.session.add(add_diary)
      db.session.commit()
    allTodo = Diary.query.all()
    return render_template("diary.html",allDiary = allTodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/todolist.html")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":       
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/todolist.html")
        

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/<location>')
def go_location(location):
    if  "news" in location:
        newsapi = NewsApiClient(api_key='75a50dd1e1bf4f7e9446b361d079abb6')
        topheadlines = newsapi.get_top_headlines(country="in")
        articles = topheadlines['articles']
        desc = []
        news = []
        img = []
        url = []
        for i in range(len(articles)):
            myarticles = articles[i]
            news.append(myarticles['title'])
            desc.append(myarticles['description'])
            if len(str(myarticles["urlToImage"])) >3:
                img.append((myarticles["urlToImage"]))
            else:
                img.append("https://shmector.com/_ph/18/412122157.png")
            url.append(myarticles['url'])
        mylist = zip(news, desc, img, url)
        return render_template(location, context=mylist)
    elif 'todo' in location:
            allTodo = Todo.query.all()
            return render_template("todolist.html",allTodo = allTodo)
    elif 'diary' in location:
        allTodo = Diary.query.all()
        return render_template("diary.html",allDiary = allTodo)
    else:
        print(location)
        return render_template(location)

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=False,host='0.0.0.0')
