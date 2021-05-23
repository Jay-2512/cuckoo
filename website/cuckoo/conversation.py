# Couldn't find a way to fetch threads using tweepy
# So the requests to the api is send using the requests module

import requests
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv("API_KEY")
bearer_token = os.getenv("BEARER_TOKEN")

# this function sends request to get the conversation_id of a tweet from its id
def getConversationId(id):
    uri = "https://api.twitter.com/2/tweets?"

    params = {"ids": id, "tweet.fields": "conversation_id"}

    bearer_header = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer {}".format(bearer_token),
        "oauth_consumer_key": consumer_key,
    }
    resp = requests.get(uri, headers=bearer_header, params=params)
    return resp.json()["data"][0]["conversation_id"]


# This function uses the conversation_id to get the thread or tweets that have the same conversation_id
def getConversation(conversation_id):
    uri = "https://api.twitter.com/2/tweets/search/recent?"
    
    # A query to return the tweets that match the conversation id alongwith the fields exppected to be returned
    # Details can be found at: 
    # 
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
    # 
    # 
    params = {
        "query": f"conversation_id:{conversation_id}",
        "expansions": "author_id",
        "tweet.fields": "in_reply_to_user_id",
        "tweet.fields": "conversation_id",
        "tweet.fields": "author_id",
        "user.fields": "username",
    }

    bearer_header = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer {}".format(bearer_token),
        "oauth_consumer_key": consumer_key,
    }
    resp = requests.get(uri, headers=bearer_header, params=params)
    return resp.json()

# this function combines the above functions and directly returns the thread from the tweet id
def getThread(id):
    return getConversation(getConversationId(id))
