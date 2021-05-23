# importing flask and auth0 modules

from functools import wraps
import json
from logging import debug
import os
from os import environ as env, getenv
from flask.globals import request
from werkzeug.exceptions import HTTPException

from .cuckoo.thread_fetch import main

from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import Response
from flask import url_for
from authlib.integrations.flask_client import OAuth

import time

# loading environment variables
load_dotenv()

def twitter_login(path, app):

    # auth0 credentials
    #
    #
    # You can get your own auth0 credentials from : https://www.auth0.com
    # For more details on getting the api and setting up the apps and routes : https://auth0.com/docs/quickstart/webapp/python
    #
    #

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


    @app.route('/output')
    def return_output():
        list = []
        # getting the user_id of the logged in user from the session.
        userinfo = session['profile']
        raw_id = userinfo['user_id']
        l = raw_id.split('|')
        uid = l[1]
        uid = int(uid)

        # path to read the output.txt file
        file_location = path + f'\\website\\templates\\{uid}output.txt'
        with open(file_location, "r") as f:
            content = f.read()

        return Response(content, mimetype='text/plain')


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

    @app.route('/login')
    def login():
        # Your callback url here
        return auth0.authorize_redirect(redirect_uri='https://cuckoo--bot.herokuapp.com/callback')

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

            # getting the user_id of the logged in user from the session.

            userinfo = session['profile']
            raw_id = userinfo['user_id']
            l = raw_id.split('|')
            uid = l[1]
            uid = int(uid)

            # calling the main method from | cuckoo\thread_fetch.py

            is_empty = main(path, uid)

            print(is_empty)

            time.sleep(1)
            if is_empty == 0:
                return render_template('twitter-thread-success.html')
            else:
                return render_template('twitter-thread-fail.html')
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
