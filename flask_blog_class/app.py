import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'



# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

#function to retreieve a post from db
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)

    return post


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #get a connection to the database
    conn = get_db_connection()

    #read all posts from the posts table in database
    posts = conn.execute('SELECT * FROM posts').fetchall()

    #close connection
    conn.close()
    
    #send posts to the index.html template to be displayed
    return render_template('index.html', posts=posts)


# route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    #determind if the page isbeing requested w a post or get request
    if request.method == 'POST':
        #get the title and content that swas submitted
        title = request.form['title']
        content = request.form['content']

        #display an error message if title or content is not submitted
        #else make a db connection and insert the blog post content
        if not title:
            flash("Title is required")
        elif not content:
            flash("Content is required")
        else:
            conn = get_db_connection()
            #insert data into db
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title,content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

#create route to edit a post, load page with a get or post method
#pass the post id as url parameter
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    #get the post from db with a select query for the post with that id
    post = get_post(id)


    #determine if the page was requested with gET or POST
        # if post process form data. get data dn validate it . update the post and rediret back to homepage

    if request.method == 'POST':
        #get the title and content that swas submitted
        title = request.form['title']
        content = request.form['content']

        #if not title or content flash error message
        if not title:
            flash ('Title is required')
        elif not content:
            flash("Content is required")
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    

    #if get then display page
    return render_template('edit.html', post=post)

app.run()