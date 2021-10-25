import os
import tweepy


def lambda_handler(event, context):

    # auth tweetpy
    auth = tweepy.OAuthHandler(os.environ["API_KEY"], os.environ["API_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"],
                          os.environ["ACCESS_TOKEN_SECRET"])

    api = tweepy.API(auth)
    api.update_status("Tweet from Lambda")
