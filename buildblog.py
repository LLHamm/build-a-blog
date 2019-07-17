from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TEXT

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:LittleRichard12@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f367c577eac03b32a77ee55aa3179723'
# pylint: disable=no-member

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.TEXT())

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog')
def index():
    entries = Blog.query.all()
    return render_template('blog.html', title='Build a Blog', entries=entries)

@app.route('/createnew', methods=['GET', 'POST'])
def create_new():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title.strip() == '' or body.strip() == '':
            flash('We need both a title and some actual text in the post.', 'error')
        else:
            blog_entry = Blog(title, body)
            db.session.add(blog_entry)
            db.session.commit()
            id = blog_entry.id
            return redirect('/showentry?id=' + str(id))        
    
    return render_template('new_entry.html', title='Create new entry')

@app.route('/showentry')
def show_entry(): 
    id = request.args.get('id', type = int)   
    blog_entry = Blog.query.filter_by(id=id).first()
    return render_template('entry.html', title = blog_entry.title, entry = blog_entry)

if __name__ == '__main__':
    app.run()