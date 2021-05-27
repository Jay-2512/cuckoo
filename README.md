# CUCKOO 🐦

## Cuckoo the twitter bot

### Web Console 💻

Ever wished about a bot which can save a twitter thread for you after having an interesting debate on twitter?🤔

Well, cuckoo can help you.😉

Mention her in the thread which you want to save, comeback and log in to the cuckoo console with your twitter id, you can simply download the thread. 😀

## Deployed code

> Cuckoo is currently not hosted anywhere

## Deploying cuckoo

- Cuckoo is built using python and tweepy
- Install the required packages and run app.py
- Make sure you have twitter developer account and also an Auth0 account
- Make sure to set the [environment variables](#environment)

### Environment

- The following environment variables must be set beforehand if you want to run cuckoo on your machine:
- Twitter API's (Get your API's from : https://developer.twitter.com/en):
  - API_KEY : Your twitter dev account api key
  - API_SECRET: Your twitter dev account api secret
  - BEARER_TOKEN: Your BearerToken
  - ACCESS_TOKEN: Your app's access token
  - ACCESS_TOKEN_SECRET: Your app's access token secret
- Auth0 API's (Get your API's from : https://www.auth0.com for more help on setting up : https://auth0.com/docs/quickstart/webapp/python):


  - A_CLIENT_ID : Your Auth0 client ID
  - A_CLIENT_SECRET : Your Auth0 client secret
  - API_BASE_URL : Your Auth0 api base url
  - ACCESS_TOKEN_URL : Your Auth0 acess token url
  - AUTHORIZE_URL : Your Auth0 authorize url

## Commiting to the repo

Do you love this project?

You think it has some bugs and know how to fix it?

Or, you think this can be improved?

You're always welcome to fork, commit and send a pull request

Any pull request, which helps to:

- Fix bugs
- Add more features

will be merged after reviews and conflict inspection from other contributors
