from flask import Flask
from .twitter_login import twitter_login
# from six.moves.urllib.parse import urlencode

def create_app(path):
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'asdanoifnow23in12fwoi3nto13123in'
    twitter_login(path, app)
    # from .auth import auth

    # app.register_blueprint(auth, url_prefix="/twitter-login")

    return app
    