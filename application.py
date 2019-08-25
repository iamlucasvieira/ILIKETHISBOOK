import os

from flask import Flask, session, render_template, request,redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *



app = Flask(__name__)

# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": " 9rvfoa1pLB0faeHA1chiww", "isbns": "9781632168146"})
# print(res.json())

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# db.init_app(app)
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# db=sqlalchemy.SQLAlchemy(app)

def main():
    # Create tables based on each table definition in `models`
    db.create_all()


@app.route("/",methods=["POST","GET"])
def index():
    return render_template("layout.html",logged=session.get('logged'),message=None,user=session.get("user"))

@app.route("/log")
def loged():
    return render_template("layout.html",logged=session.get('logged'))


@app.route("/search", methods=["POST"])
def searchpage():

    searchitem = request.form.get("search")
    if searchitem != "":
        return redirect(url_for("search",search=searchitem))
    else:
        return render_template("search.html", logged=session.get('logged'), books=[], user=session.get("user"),
                               message=None)

@app.route("/search/<string:search>", methods=["POST","GET"])
def search(search):
    books = db.execute("SELECT * FROM books WHERE lower(title) LIKE :search OR lower(author) LIKE :search OR isbn LIKE :search",{"search":f"%{search.lower()}%"}).fetchall()
    if books == []:
        return render_template("search.html", logged=session.get('logged'), books=books, user=session.get("user"),
                               message=f"0 books found!")
    return render_template("search.html",logged=session.get('logged'), books=books,user=session.get("user"),message=None)

@app.route("/signupfunc")
def signupfunc():
    return render_template("signup.html",logged=session.get('logged'), message=None)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    pass1 = request.form.get("password")
    pass2 = request.form.get("confirmpassword")
    if name == "":
        message = "Error: Name not informed"
        return render_template("signup.html", logged=session.get('logged'), message=message)
    if email == "":
        message = "Error: Email not informed"
        return render_template("signup.html", logged=session.get('logged'), message=message)

    if len(str(pass1)) != 0 and pass1==pass2:
        session["logged"]=True
        return()
        newuser = Signup(name=name,email=email,password=pass1)
        db.add(newuser)
        db.commit()
        session["user"] = newuser
        session["name"]=newuser.name
        session["user_id"] = newuser.id
        message = f"{ session.get('name')}, your Account has been created"
        return render_template("layout.html",logged=session.get('logged'),message=message,user=session.get("user"))
    else:
        session["logged"]=False
        message = "Error: Passwords do not match"
        return render_template("signup.html", logged=session.get('logged'),message=message)


@app.route("/logout")
def logout():
    session.pop("name")
    session.pop("user")
    session["logged"] = False
    message = "You have logged out"
    return render_template("layout.html",logged=session.get('logged'), message=message)


@app.route("/login")
def login():
    return render_template("login.html",logged=session.get( 'logged'),message=None)

@app.route("/trylog", methods=["POST"])
def trylog():
    email = request.form.get("email")
    passw = request.form.get("password")
    user = db.execute("SELECT * FROM signup WHERE email = :email AND password = :pass",{"email": email, "pass":passw}).fetchone()
    session["user"] = user
    if user is None:
        return render_template("login.html", logged=session.get('logged'), message="Email and Password doesn't match")
    session["logged"] = True
    session["name"] = user.name
    return render_template("layout.html",logged=session.get('logged'), message=session.get( 'name'),user=user)


@app.route("/<string:book>",methods=["POST","GET"])
def book(book):
    book = db.execute("SELECT * FROM books WHERE isbn=:book",
                       {"book": book}).fetchone()
    review = db.execute("SELECT * FROM reviews JOIN signup ON reviews.signup_id = signup.id WHERE book_id=:book ORDER BY reviews.id DESC",
                       {"book": book.id}).fetchall()

    if session.get("user") != None:
        userhasreview = db.execute("SELECT * FROM reviews WHERE signup_id =:user_id AND book_id=:book",{"user_id":session.get("user").id,"book":book.id}).fetchone()
    else:
        userhasreview = None
    return render_template("book.html",logged=session.get('logged'),book=book,user=session.get("user"),reviews=review,userhasreview=userhasreview)

    # if Signup.query.filter_by(email=email).count != 0 :
    #     return render_template("login.html",logged=session.get('logged'), message=None)
    # else:
    #     return redirect(url_for("search"))

@app.route("/post/<string:book>",methods=["POST","GET"])
def post(book):

    book_id = db.execute("SELECT id FROM books WHERE isbn=:book",
                      {"book": book}).fetchone()[0]
    user_id = session.get("user").id
    rating = request.form.get("inlineRadioOptions")
    message = request.form.get("userreview")
    if rating==None:
        return redirect(url_for("book",book=book))
    newpost = Reviews(rating=rating,message=message,book_id=book_id,signup_id=user_id)
    db.add(newpost)
    db.commit()
    session["message"] = message
    return redirect(url_for("book",book=book))


@app.route("/delete/<string:post_id>/<string:book_isbn>",methods=["POST"])
def delete(post_id,book_isbn):
    # deletereview = db.execute("SELECT * FROM reviews WHERE id=:postid",
    #                    {"postid": post_id}).fetchall()
    # db.delete(deletereview)
    # db.commit()
    db.execute("DELETE FROM reviews WHERE id=:postid", {"postid": post_id})
    db.commit()
    return redirect(url_for("book",book=book_isbn))


if __name__ == "__main__":
    with app.app_context():
        main()