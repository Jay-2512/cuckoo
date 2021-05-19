from functools import wraps
import json
from logging import debug
import os
from os import environ as env, getenv
from flask.globals import request
from werkzeug.exceptions import HTTPException

from .cuckoo.thread_fetch import main

# from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

import time

def twitter_login(app):
    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id= os.getenv('A_CLIENT_ID'),
        client_secret= os.getenv('A_CLIENT_SECRET'),
        api_base_url=os.getenv('API_BASE_URL'),
        access_token_url=os.getenv('ACCESS_TOKEN_URL'),
        authorize_url=os.getenv('AUTHORIZE_URL'),
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    # Here we're using the /callback route.
    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/twitter-login')
    def logged_in():
        return render_template('twitter-thread.html')


    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/dashboard')
        # return redirect(url_for('logged_in'))

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri='http://127.0.0.1:5000/callback')

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'profile' not in session:
                # Redirect to Login page here
                return redirect('/')
            return f(*args, **kwargs)
        return decorated

    @app.route('/dashboard', methods=['GET', 'POST'])
    @requires_auth
    def dashboard():
        if request.method == 'POST':
            twitter_handle = request.form.get('twitter_handle')
            print(twitter_handle)
            main(twitter_handle)
            time.sleep(1)
            return render_template('twitter-thread.html')
        else:
            return render_template('dashboard.html',
                                userinfo=session['profile'],
                                userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


    @app.route('/logout')
    def logout():
        # Clear session stored data
        session.clear()
        # Redirect user to logout endpoint
        return redirect(url_for('home'))


    app.run(debug=True)