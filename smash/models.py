import sqlite3

class Model(object):
    #Name of the table to be created
    tablename = "abstractmodel"

    #Attributes are tuples - attribute name, data type, other requirements
    id = ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT")


class Quote(Model):
    tablename = "quotes"

    id = ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT")
    rating = ("rating", "INTEGER", "NOT NULL")
    content = ("content", "TEXT", "NOT NULL")


class Tag(Model):
    tablename = "tags"

    id = ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT")
    name = ("name", "TEXT", "UNIQUE NOT NULL")


class TagsToQuotes(Model):
    tablename = "tagsToQuotes"

    id = ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT")
    tag_id = ("tagid", "INTEGER", "NOT NULL")
    quote_id = ("quoteid", "INTEGER", "NOT NULL")


def init_models(db):
    import logging
    logger = logging.getLogger(__name__)

    for model in Model.__subclasses__():
        columns = [x for x in model.__dict__ if '__' not in x and x !=
                   'tablename']

        try:
            db.create_table(
                    model.tablename,
                    ','.join([' '.join(model.__dict__[x]) for x in columns])
            )
            logger.info("Created table in the database:"
                        " {}".format(model.tablename))
        except:
            #If we can't create a table here, it means it's already in the
            #database, so we can skip it
            pass
