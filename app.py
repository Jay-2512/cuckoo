from logging import debug
from website import create_app
from website.twitter_login import twitter_login
import os


path = os.getcwd()

app = create_app(path)

if __name__ == '__main__':
    app.run(debug=True)