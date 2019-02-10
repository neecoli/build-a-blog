from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = 'buildablog'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, name, body):
        self.title = title
        self.body = body
        



blogs = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blogname = request.form['blog']
        blogs.append(blogname)
        new_blog = Blog(blogname)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    return render_template('addblog.html',title="Add a Blog Entry", blogs=blogs) 

#The /blog route displays all the main blog posts.
#@app.route('/blog')




#submit a new post at the /newpost route; after submitting new post
#app displays main blog page
#@app.route('/newpost')

if __name__ == '__main__':
    app.run()