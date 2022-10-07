from app import *
from models import *
from flask import render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import update


@app.route('/main', methods=["GET", "POST"])
def main():
    ROWS_PER_PAGE = 10
    page = request.args.get('page', 1, type=int)
    article = Article.query.order_by(Article.date.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
    users = Users.query.all()

    return render_template('main.html', article=article, users=users)


@app.route('/main/like/<int:id>', methods=["GET", "POST"])
def like(id):
    like1 = Likes.query.filter(Likes.title == id).first()
    # name_of_title = like1.i_like
    user = Likes.query.filter(Likes.user == session.get('user')['id']).first()
    # usr = user.user
    try:
        name_of_title = like1.i_like
        usr = user.user
    except AttributeError:
        user_id = session.get('user')['id']
        likes = Likes(i_like=True, i_dislike=False, user=user_id, title=id)
        db.session.add(likes)
        db.session.commit()
        return 'Liked!'
    if request.method == 'GET' and name_of_title is True and session.get('user')['id'] == usr:
        user_id = session.get('user')['id']
        Likes.query.filter_by(i_like=1, user=user_id, title=id).update(dict(i_like=0))
        db.session.commit()
        return 'Unliked:('
    elif request.method == 'GET':
        user_id = session.get('user')['id']
        Likes.query.filter_by(i_like=0,user=user_id, title=id).update(dict(i_like=1, i_dislike=0))
        db.session.commit()
        return 'Liked!'
    return redirect('/main')


@app.route('/main/dislike/<int:id>', methods=["GET", "POST"])
def dislike(id):
    dislike1 = Likes.query.filter(Likes.title == id).first()
    user = Likes.query.filter(Likes.user == session.get('user')['id']).first()
    # usr = user.user
    try:
        name_of_title = dislike1.i_dislike
        usr = user.user
    except AttributeError:
        user_id = session.get('user')['id']
        likes = Likes(i_like=False, i_dislike=True, user=user_id, title=id)
        db.session.add(likes)
        db.session.commit()
        return 'Disliked!'
    if request.method == 'GET' and name_of_title is True and session.get('user')['id'] == usr:
        user_id = session.get('user')['id']
        Likes.query.filter_by(i_dislike=1, user=user_id, title=id).update(dict(i_dislike=0))
        db.session.commit()
        return 'Undisliked:('
    elif request.method == 'GET':
        user_id = session.get('user')['id']
        Likes.query.filter_by(i_dislike=0, user=user_id, title=id).update(dict(i_dislike=1, i_like=0))
        db.session.commit()
        return 'Disliked!'
    return redirect('/main')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('authorization'))


@app.route('/create', methods=["GET", "POST"])
def article():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        article = Article(title=title, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/main')
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
            return redirect('/main')
        except:
            return "Error"
    return render_template('posts_detail.html', article=articles, comments=comments)


@app.route('/', methods=["GET", "POST"])
def regis():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        hash = generate_password_hash(password)
        reg = Users(login=login, password=hash)
        db.session.add(reg)
        db.session.commit()
        login = request.form['login']
        form = request.form
        user = Users.query.filter(Users.login == form['login']).filter(Users.password == form['password']).first()
        if user is not None:
            session['logged_in'] = True
            session['user'] = user.serialize
        return redirect('/authorization')
    return render_template('registration.html')


@app.route('/authorization', methods=["GET", "POST"])
def authorization():
    if request.method == "POST":
        password = request.form['password']
        form = request.form
        user = Users.query.filter(Users.login == form['login']).first()
        psswd = user.password
        chek = check_password_hash(str(psswd), str(password))
        if user is not None and chek is True:
            session['logged_in'] = True
            session['user'] = user.serialize
        else:
            return 'Login or password is not correct!'
        return redirect('/main')
    return render_template('authorization.html')



