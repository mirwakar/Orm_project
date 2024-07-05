from datetime import datetime
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DATABASE_URL"] = "db.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///article.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.Date, default=datetime.now)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title")
        if title:
            a1 = Article(title=title)
            db.session.add(a1)
            db.session.commit()
            message = "Article successfully created"
        else:
            message = "Title cannot be empty"
        a1 = Article.query.all()
        return render_template("home.html", articles=a1, message=message)
    else:
        a1 = Article.query.all()
        return render_template("home.html", articles=a1)


@app.route("/delete", methods=["POST"])
def delete():
    article_id = request.form.get("id")
    if article_id:
        article = Article.query.get(article_id)
        if article:
            db.session.delete(article)
            db.session.commit()
            message = "Article successfully deleted"
        else:
            message = "Article does not exist"
    else:
        message = "ID cannot be empty"
    articles = Article.query.all()
    return render_template("home.html", articles=articles, message=message)


@app.route("/update", methods=["POST"])
def update():
    article_id = request.form.get("id")
    title = request.form.get("title")
    if article_id:
        article = Article.query.get(article_id)
        if article:
            article.title = title
            db.session.commit()
            message = "Article successfully updated"
        else:
            message = "Article does not exist"
    else:
        message = "ID cannot be empty"
    articles = Article.query.all()
    return render_template("home.html", articles=articles, message=message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
