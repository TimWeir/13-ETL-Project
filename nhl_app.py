from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_nhl

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/nhl_app"
mongo = PyMongo(app)



# create route that renders index.html template
@app.route("/")
def index():
    data = mongo.db.nhlproject.find_one()
    i=0
    print(data)
    print("==")
    return render_template("index.html", data=data, i=i)


@app.route("/scrape")
def scraper():
    data = scrape_nhl.scrape()
    print(data)
    mongo.db.nhlproject.update({}, data, upsert=True)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)