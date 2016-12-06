import datetime
import logging
from flask import render_template, Markup

from smash import app, conf, db

logger = logging.getLogger(__name__)


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
    quotes = [(q[0], q[1], bytes(Markup.escape(q[2]), 'utf-8').decode('utf-8').replace('\n', '</br>')) for q in quotes]

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

        tags = db.select("tagsToQuotes", "tagid", "quoteid='{}'".format(quote[0][0]))
        tags_str = []
        for tag in tags:
            tags_str.append(db.select("tags", "name", "id='{}'".format(tag[0]))[0][0])

        quote = [
            (
                quote[0][0],
                quote[0][1],
                bytes(Markup.escape(quote[0][2]), 'utf-8').decode('utf-8').replace('\n', '</br>'),
                tags_str
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
    if request.method == 'POST':
        return 'success'
    else:
        return 'Invalid request.'
