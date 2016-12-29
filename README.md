# smash
a bash.org clone built with Flask

## How to run
This program is designed to be easy to deploy via Heroku. It can also run locally.
Database is stored locally in an sqlite file.

First, you have to edit the config file (`config.json`). `DBNAME` needs to be a valid filename for the database. `APPNAME` is the name that will be displayed in the title bar in the browser, while `APPBRAND` is the name that will be displayed in the navbar on every page.

`SECRETKEY` will be used to encrypt and sign session cookies, so it needs to be a cryptographically-secure random string. `ADMINSECRET` will be used to elevate privileges to allow approving and deleting new quotes. There are no user accounts since there are no user-specific functionalities.

`APPNAME` and `APPBRAND` will be loaded from the environment if they're left empty in the config.

After basic config is done, run this to start the server:

```
python run.py
```

The program looks for `HEROKU` in the environment; if that variable is equal to 1, it interprets this as a sign that it's running in a production environment and starts in the externally visible mode with debug turned off. It also needs the `PORT` environment variable to have some sensible value; this is configured automatically when deploying on heroku.

The first time it's started it will create the local database and all required tables, as specified by models. After that it's ready to be used.

All logging is done by printing to stdout - heroku adds that to the app logs visible in the dashboard.
