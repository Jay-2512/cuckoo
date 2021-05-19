from logging import debug
from website import create_app
from website.twitter_login import twitter_login


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)