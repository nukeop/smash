from smash import db


tags_to_quotes = db.Table(
    'tagsToQuotes',
    db.Column('tagid', db.Integer, db.ForeignKey('tags.id')),
    db.Column('quoteid', db.Integer, db.ForeignKey('quotes.id'))
)


class Quote(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    content = db.Column(db.String(), nullable=False)
    approved = db.Column(db.Boolean)
    author_ip = db.Column(db.String(), nullable=False)
    time = db.Column(db.String(), nullable=False)
    tags = db.relationship(
        'Tag',
        secondary=tags_to_quotes,
        backref=db.backref('quotes', lazy='dynamic')
    )


    def __init__(self, content, author_ip, time):
        self.rating = 0
        self.content = content
        self.approved = False
        self.author_ip = author_ip
        self.time = time


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)


    def __init__(self, name):
        self.name = name
