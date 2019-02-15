from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'buildablog'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        

#blogs = []

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')


#The /blog route displays all the main blog posts.
@app.route('/blog', methods=['POST', 'GET'])
def display_mainblog():
    
    #if user clicks on blog, redirect to individual blog page
    #query db for the blog entry
    
    if request.args:
        blog_id = request.args.get('id')
        #oneblog = Blog(title, body)
        blog = Blog.query.get(blog_id)
            
        return render_template('individualblog.html', blogname=blog.title, blogentry=blog.body)

    blogs = Blog.query.all()
    return render_template('mainblog.html', blogs=blogs)


#submit a new post at the /newpost route; after submitting new post
#app displays main blog page
@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        return render_template('addblog.html')
    
    blogname = request.form['title']
    blogentry = request.form['body']
    new_blog = Blog(blogname, blogentry)
    db.session.add(new_blog)
    db.session.commit()
    
    titleerror = ''
    entryerror = ''

    if (not blogname) or (blogname.strip() == ""):
        titleerror = "Enter a Title"
        
    if (not blogentry) or (blogentry.strip() == ""):
        entryerror = "Enter a blog"
    
    if not titleerror and not entryerror:
        #case2: after adding post, go to individual post page
        return render_template('individualblog.html', blogname=blogname, blogentry=blogentry)
        #return render_template('mainblog.html', blogs=blogs)
    else:
        return render_template('addblog.html', titleerror=titleerror, entryerror=entryerror)
        #return redirect("/?error=" + error)

if __name__ == '__main__':
    app.run()