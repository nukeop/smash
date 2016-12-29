import datetime
import logging
import psycopg2
from flask import render_template, Markup, request, abort, session

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
    quotes = reversed(db.select("quotes", "id, rating, content", "approved"))
    quotes = [(q[0], q[1], unicode(Markup.escape(q[2])).replace('\n', '</br>')) for q in quotes]

    quotes_tags = []

    for quote in quotes:
        tags = db.select("tagsToQuotes", "tagid", "quoteid='{}'".format(quote[0]))
        tags_str = []
        for tag in tags:
            tags_str.append(db.select("tags", "name", "id='{}'".format(tag[0]))[0][0])

        quotes_tags.append(
            (
                quote[0],
                quote[1],
                quote[2],
                tags_str
            )
        )

    return render_template(
        "latest.html",
        appname=conf.config['APPNAME'],
        appbrand=conf.config['APPBRAND'],
        title="Latest",
        quotes=quotes_tags
    )


@app.route('/quote/<int:id>')
def quote(id):
    quote = db.select("quotes", "id, rating, content", "id='{}'".format(id))
    if len(quote)<1:
        return render_template(
            "message.html",
            alertclass="alert-warning",
            message="No such quote."
        )
    else:

        tags = db.select("tagsToQuotes", "tagid", "quoteid='{}'".format(quote[0][0]))
        tags_str = []
        for tag in tags:
            tags_str.append(db.select("tags", "name", "id='{}'".format(tag[0]))[0][0])

        quote = [
            (
                quote[0][0],
                quote[0][1],
                unicode(Markup.escape(quote[0][2])).replace('\n', '</br>'),
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

            cur = db.insert(
                "quotes",
                "rating, content, approved, author_ip, time",
                "?, ?, ?, ?, ?",
                (0, quote_body, 0, request.remote_addr, datetime.datetime.now().strftime("%H:%M:%S %d/%m/%y"),)
            )
            qid = cur.lastrowid

            for tag in quote_tags:
                tid = -1
                try:
                    cur = db.insert(
                        "tags",
                        "name",
                        "?",
                        (tag,)
                    )
                    tid = cur.lastrowid
                except psycopg2.IntegrityError:
                    logger.warning("Tag {} already exists".format(tag))

                if tid != -1:
                    try:
                        db.insert(
                            "tagsToQuotes",
                            "tagid, quoteid",
                            "?, ?",
                            (tid, qid)
                        )
                    except psycopg2.Error:
                        logger.warning("Database error while inserting into tagsToQuotes")
                        return render_template(
                            "message.html",
                            alertclass="alert-danger",
                            message="Could not add your quote. Try again later."
                        )
            return render_template(
                "message.html",
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
