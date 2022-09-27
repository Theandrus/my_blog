from app import app, db
from models import Users, Article, Comments
from flask import render_template, request, session, redirect, url_for

@app.route('/main', methods=["GET", "POST"])
def main():
    article = Article.query.order_by(Article.date.desc()).all()
    users = Users.query.all()
    return render_template('main.html', article=article, users=users)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('main'))


@app.route('/create', methods=["GET", "POST"])
def article():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        article = Article(title=title, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error"
    else:
        return render_template('create.html')


@app.route('/posts/<int:id>', methods=["GET", "POST"])
def posts_detail(id):
    articles = Article.query.get(id)
    comments = Comments.query.filter_by(article_id=id)
    if request.method == "POST":
        text = request.form['text']
        article_id = id
        comments = Comments(text=text, article_id=article_id)
        try:
            db.session.add(comments)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error"
    return render_template('posts_detail.html', article=articles, comments=comments)


@app.route('/', methods=["GET", "POST"])
def regis():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        reg = Users(login=login, password=password)
        db.session.add(reg)
        db.session.commit()
        login = request.form['login']
        form = request.form
        user = Users.query.filter(Users.login == form['login']).filter(Users.password == form['password']).first()
        if user is not None:
            session['logged_in'] = True
            session['user'] = user.serialize
        return redirect('/main')
    return render_template('registration.html')


@app.route('/authorization', methods=["GET", "POST"])
def authorization():
    if request.method == "POST":
        login = request.form['login']
        form = request.form
        user = Users.query.filter(Users.login == form['login']).filter(Users.password == form['password']).first()
        if user is not None:
            session['logged_in'] = True
            session['user'] = user.serialize
        else:
            return "Login or password not correct!"
        return redirect('/main')
    return render_template('authorization.html')



