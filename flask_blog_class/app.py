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

app.run()