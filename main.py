from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Testing'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    post_time = db.Column(db.DateTime)

    def __init__(self, title, body, post_time=None):
        self.title = title
        self.body = body
        if post_time is None:
            post_time = datetime.utcnow()
        self.post_time = post_time

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    blogs = Blog.query.all()
    return render_template('blog.html', title='My Posts', blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def post():
    error = False
    title_error = ''
    body_error = ''

    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']

        if len(post_title) < 1:
            title_error = "Give your post a title!"
            error = True

        if len(post_body) < 1:
            body_error = "Your blog needs words...Write something!"
            error = True

        if error == True:
            return render_template('newpost.html', title='Write a new post', error = error, title_error = title_error, body_error = body_error)
    
        new_post = Blog(post_title, post_body)
        db.session.add(new_post)
        db.session.commit()
        post_id = str(new_post.id)
        flash("Success! You published a blog post.")
        return redirect('/select_blog?id=' + post_id)

    return render_template('/newpost.html', title="Write a new post", error=error, title_error=title_error, body_error=body_error)

@app.route('/select_blog', methods=['GET', 'POST'])
def select():
    post_id = request.args.get('id')
    blog_post = Blog.query.filter_by(id=post_id).first()

    return render_template('select_blog.html', title="My post", select_blog=blog_post)

if __name__ == "__main__":
    app.run()