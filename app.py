from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", marsdata=mars)

@app.route("/scrape")   
def scrape():
    mars=scrape_mars.scrape_all()
    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

