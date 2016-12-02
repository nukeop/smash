from flask import render_template

from smash import app, conf, db


@app.route('/')
def index():
    return render_template(
        "index.html",
        appname=conf.config["APPNAME"],
        title="Quotes",
        msg="Landing page!"
    )


@app.route('/latest')
def latest():
    quotes = reversed(db.select("quotes", "id, rating, content"))
    quotes = [(q[0], q[1], q[2].replace('<', '&lt;').replace('>', '&gt;').replace('\n', '</br>')) for q in quotes]

    return render_template(
        "latest.html",
        appname=conf.config["APPNAME"],
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
        appname=conf.config["APPNAME"],
        title="Latest",
        quotes=quote
    )


@app.route('/tags')
def tags():
    return render_template(
        "tags.html",
        appname=conf.config["APPNAME"],
        title="Tags"
    )
