# This module deals with creation of api object for tweepy using the api keys

import tweepy
import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger()

#load env files
load_dotenv()

# This function creates & returns an api object from the api keys stored in environment variables
#  and it also verifies the credentials
def create_api(path):
    consumer_key =  os.getenv("API_KEY")
    consumer_secret = os.getenv("API_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
