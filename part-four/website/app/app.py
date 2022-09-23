from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TalksModel(db.Model):
    __tablename__ = 'talks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    abstract = db.Column(db.String())

    def __init__(self, title, abstract):
        self.title = title
        self.abstract = abstract

    def __repr__(self):
        return f"<Talk {self.title}>"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/portfolio')
def portfolio():
    return render_template("portfolio.html")

@app.route('/talks', methods=['GET'])
def talks():
    talks = TalksModel.query.all()
    results = [
        {
            "title": talk.title,
            "abstract": talk.abstract,
        } for talk in talks]

    return {"count": len(results), "talks": results}
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True) 