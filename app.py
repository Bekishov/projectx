from flask import Flask, render_template, request, redirect
from models import db, Post,MyUser
import os
from flask_login import login_required, current_user, LoginManager, login_user,logout_user

app = Flask(__name__, static_url_path='/static/')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
app.secret_key = os.urandom(24)

@login_manager.user_loader
def load_user(user_id):
    return MyUser.select().where(MyUser.id==int(user_id)).first()

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response



@app.route('/')
def index():
    all_posts = Post.select()
    return render_template('index.html', posts = all_posts)

@app.route('/create/', methods =('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        Post.create(
            title = title,
            author =  current_user,
            description = description
        )
        return redirect('/')
    return render_template('create.html')

@app.route('/<int:id>/')
def post_detail(id):
    post = Post.select().where(Post.id==id).first()
    if post:
        return render_template('post_detail.html', post=post)
    return f'Post with id = {id} does not exist'

@app.route('/<int:id>/update', methods = ('GET', "POST"))
@login_required
def update(id):
    post = Post.select().where(Post.id==id).first()
    if request.method == 'POST':
        if current_user == Post.author:
            if post:
                title = request.form['title']
                description = request.form['description']
                obj = Post.update({
                    Post.title: title,
                    Post.description:description
                }).where(Post.id==id)
                obj.execute()
                return redirect(f'/{id}/')
            return f'Post with id = {id} does not exist'
        return f'You dont have permission to update this post'
    return render_template('update.html', post=post)

@app.route('/<int:id>/delete', methods = ('GET', "POST")) 
@login_required 
def delete(id): 
    post = Post.select().where(Post.id==id).first() 
    if post: 
        if current_user == post.author: 
            if request.method == 'POST': 
                post.delete_instance() 
                return redirect('/') 
            return render_template('delete.html', post=post) 
        else: 
            return "You don't have permission to delete this post." 
    else: 
        return f'Post with id = {id} does not exist'


@app.route('/register/',methods = ('GET','POST'))
def register():
    if request.method=='POST':
        email = request.form['email']
        name = request.form['name']
        second_name = request.form['second_name']
        password = request.form['password']
        age = request.form['age']

        if len(password) >= 8:
            MyUser.create(
                email=email,
                name=name,
                second_name=second_name,
                password=password,
                age=age
            )
            return redirect('/login/')
        return 'пароль меньше 8символов'
    return render_template('register.html')


@app.route('/login/', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = MyUser.select().where(MyUser.email==email).first()
        if password==user.password:
            login_user(user)
            return redirect('/profile/')
        return redirect('/register/')
    return render_template('login.html')

@app.route('/profile/')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/login/')





if __name__ == '__main__':
    app.run(debug=True)