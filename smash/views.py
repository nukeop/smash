import datetime
import logging
import psycopg2
from flask import render_template, Markup, request, abort, session

from smash.models_sqlalchemy import *
from smash import app, conf, db

logger = logging.getLogger(__name__)


def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S %d/%m/%y")


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


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        if request.form["secret"] == conf.config['ADMINSECRET']:
            session['authorized'] = True

    return render_template(
        "login.html",
        authorized=session.get('authorized', None),
        appname=conf.config['APPNAME'],
        appbrand=conf.config['APPBRAND']
    )


@app.route('/latest')
def latest():
    quotes = Quote.query.filter_by(approved=True).order_by(Quote.id.desc()).all()

    # Replace line breaks with html breaks and escape special characters
    for quote in quotes:
        quote.content = str(Markup.escape(quote.content)).replace('\n', '</br>')

    return render_template(
        "latest.html",
        appname=conf.config['APPNAME'],
        appbrand=conf.config['APPBRAND'],
        title="Latest",
        quotes=quotes
    )


@app.route('/quote/<int:id>')
def quote(id):
    quote = Quote.query.filter_by(id=id, approved=True).first()

    if quote is None:
        return render_template(
            "message.html",
            alertclass="alert-warning",
            message="No such quote."
        )
    else:
        quote.content = str(Markup.escape(quote.content)).replace('\n', '</br>')
        return render_template(
            "latest.html",
            appname=conf.config['APPNAME'],
            appbrand=conf.config['APPBRAND'],
            title="Quote #{}".format(quote.id),
            quotes=[quote,]
        )


@app.route('/tags')
def tags():
    tags = [x[0] for x in db.select("tags", "name")]

    return render_template(
        "tags.html",
        appname=conf.config['APPNAME'],
        appbrand=conf.config['APPBRAND'],
        title="Tags",
        tags=tags
    )


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        return render_template(
            "message.html",
            alertclass="alert-warning",
            message="Not implemented yet. "
        )
    else:
        return 'Invalid request.'


@app.route('/add', methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        if request.form['submit'] == "Submit":
            quote_body = request.form["newquote"]
            quote_tags = request.form["tags"].split(',')

            quote = Quote(quote_body, request.remote_addr, timestamp())
            quote_tags = [Tag(tag) for tag in quote_tags]

            quote.tags.extend(quote_tags)

            db.session.add(quote)
            db.session.commit()

            return render_template(
                "message.html",
                appname=conf.config['APPNAME'],
                appbrand=conf.config['APPBRAND'],
                alertclass="alert-success",
                message="Quote added succesfully. It will need to be reviewed by the administrators before it shows up."
            )

        elif request.form['submit'] == "Preview":
            return str(request.form)
        else:
            abort(501)

    elif request.method == 'GET':
        return render_template(
            "add.html",
            appname=conf.config['APPNAME'],
            appbrand=conf.config['APPBRAND'],
            title="Add new"
        )
