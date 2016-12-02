import os
from smash import app, conf

if __name__=='__main__':
    if 'HEROKU' in conf.config and conf.config['HEROKU']==1:
        app.run(host= '0.0.0.0', port=os.environ['PORT'])
    else:
        app.run(debug=True)
