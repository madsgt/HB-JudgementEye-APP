"""Movie Ratings."""

import jinja
from jinja2 import StrictUndefined


from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask import(Flask, render_template, redirect, request, flash, session)

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/register", methods=["GET"])
def register_form():
    

    return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_process():
    """Accept form data"""
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

       

    user_exists = User.query.filter_by(email=email).first()
    user = User(email=email, password=password, age=age, zipcode=zipcode)
    
    if user.email in user_exists.email:
        
        flash("User %s already exists!!" %email)
    else:
        db.session.add(user)
        flash("User %s added!!" % email)

    db.session.commit()

    # need to figure out a way to stop duplication of registration

      
    return redirect("/login")

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""
    return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def process_login():
    """Process log in form"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Not a valid user")
        return redirect("/login")

    if user.password != password:
        flash("Not a valid password")
        return redirect("/login")

    session["logged_in"] = user.email
    flash("already logged in")
    return redirect("/")


@app.route('/logout')
def logout():
    "User logs out"

    del session["logged_in"]
    flash("User logged out!")
    return redirect("/")


@app.route("/users")
def user_list():
    """Show list of users"""    

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/users/<int:user_id>")
def user_details(user_id):

    user = User.query.get(user_id)
    return render_template("user.html", user=user)

@app.route("/movies")
def list_movies():
    """Show list of movies"""
    movies = Movie.query.order_by('title').all()
    return render_template("movies_list.html", movies=movies)

@app.route("/movies/<int:movie_id>")
def movie_details(movie_id):
    """Show details of a movie"""
    movie = Movie.query.get(movie_id)
    return render_template("movie_details.html", movie=movie)







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
