import os

from flask import Flask, session, render_template
from waitress import serve
import requests
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": " 9rvfoa1pLB0faeHA1chiww", "isbns": "9781632168146"})
# print(res.json())

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("layout.html",title="logged")

@app.route("/log")
def loged():
    return render_template("layout.html",title="notlogged")

@app.route("/search")
def search():
    return render_template("search.html",title="logged", name=range(10))

@app.route("/signup")
def signup():
    return render_template("signup.html",title="notlogged")

if __name__ == "__main__":
    serve(app)