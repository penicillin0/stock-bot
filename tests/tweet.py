import os
from dotenv import load_dotenv
import tweepy
import yfinance as yf
import json
import datetime
import pytz


def get_marumoji(val: int) -> str:
    maru_date = "①".encode("UTF8")
    maru_code = int.from_bytes(maru_date, 'big')
    maru_code += val - 1
    return maru_code.to_bytes(4, "big").decode("UTF8")


# auth tweetpy
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(os.path.normpath(env_path))
auth = tweepy.OAuthHandler(os.environ["API_KEY"], os.environ["API_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"],
                      os.environ["ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth)


# get core30 data
core_30: dict = json.load(open('../data/core30.json', 'r'))
core_30_str = '.T '.join(core_30.keys()) + '.T'
core_30_df = yf.download(core_30_str, period='1d', group_by='ticker')


# make tweets
tweets = []
sentences = []
sentence = ''
for stock_code, stock_name in core_30.items():
    stock_data = core_30_df[stock_code + '.T']
    open_place = round(stock_data.Open[0], 1)
    close_place = round(stock_data.Close[0], 1)
    place_diff = round(close_place - open_place, 1)
    price_diff_ratio_percent = round(place_diff / close_place * 100, 2)

    sign = '+' if place_diff > 0 else ''

    sentence += f'{stock_name}({stock_code})\n'
    sentence += f'{close_place}({sign}{price_diff_ratio_percent}%)\n'
    sentence += '\n'

    if len(sentence) > 120:
        tweets.append(sentence)
        sentence = ''


# tweet
now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
month, day = now.month, now.day

for i, tweet in enumerate(tweets):
    tweet_content = str(month)+'/'+str(day) + ' Core30-' + \
        get_marumoji(i + 1) + '\n\n' + tweet
    if i == 0:
        rep = api.update_status(tweet_content)
    else:
        rep = api.update_status(status=tweet_content,
                                in_reply_to_status_id=rep.id)
