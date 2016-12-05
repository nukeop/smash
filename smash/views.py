import datetime
from flask import render_template

from smash import app, conf, db


@app.route('/')
def index():

    welcome = "<p>Welcome to the quote archive.</p>"
    news = ("<p><b>{}</b></p><h4>{} running on smash quote database"
            " engine launched today</h4>").format(
                datetime.datetime.now().strftime("%d/%m/%y"),
                conf.config['APPNAME']
            )

    return render_template(
        "index.html",
        appname=conf.config['APPNAME'],
        appbrand=conf.config['APPBRAND'],
        title="Quotes",
        welcometext=welcome,
        newstext=news
    )


@app.route('/latest')
def latest():
    quotes = reversed(db.select("quotes", "id, rating, content"))
    quotes = [(q[0], q[1], q[2].replace('<', '&lt;').replace('>', '&gt;').replace('\n', '</br>')) for q in quotes]

    return render_template(
        "latest.html",
        appname=conf.config['APPNAME'],
        appbrand=conf.config['APPBRAND'],
        title="Latest",
        quotes=quotes
    )


@app.route('/quote/<int:id>')
def quote(id):
    quote = db.select("quotes", "id, rating, content", "id='{}'".format(id))
    if len(quote)<1:
        return "No such quote."
    else:
        quote = [
            (
                quote[0][0],
                quote[0][1],
                quote[0][2],replace('<', '&lt;').replace('>', '&gt;').replace('\n', '</br>')
            )
        ]
        return render_template(
        "latest.html",
        appname=conf.config['APPNAME'],
        appbrand=conf.config['APPBRAND'],
        title="Latest",
        quotes=quote
    )


@app.route('/tags')
def tags():
    return render_template(
        "tags.html",
        appname=conf.config['APPNAME'],
        appbrand=conf.config['APPBRAND'],
        title="Tags"
    )


@app.route('/search', methods=['POST'])
def search():
    pass
