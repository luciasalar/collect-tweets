import os
import tweepy as tw
import pandas as pd
from ruamel import yaml
import csv
import pprint
import datetime
import datetime as dt
import gc
import time

def load_experiment(path_to_experiment):
    """load experiment"""
    data = yaml.safe_load(open(path_to_experiment))
    return data


class CollectTweets:
    """Collect posts via pushshift."""

    def __init__(self):
        '''define the main path'''
        self.datapath = '/disk/data/share/s1690903/collect_tweets/data/'


    # def __get_date(self, time):
    #     """convert timestamp to time"""

    #     t = datetime.datetime.fromtimestamp(time)
    #     return t.strftime('%m/%d/%Y/%H:%M:%S')

    def ___handles(self, filename):
        """Read post id files"""

        handles = pd.read_csv(self.datapath + filename)#'Anxiety_postid.csv'
        return handles

    def collect_tweets(self, handlesFile, outputfile):
        """Collect Tweets"""

        # read handle list
        handles = self.___handles(handlesFile)

        # variable names
        file_exists = os.path.isfile(self.datapath + outputfile)

        if not file_exists:
            f = open(self.datapath + outputfile, 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer_top.writerow(["user_id"] + ["tweet_id"] + ["text"] + ["created_at"] + ["retweet_count"] + ["favorited"]+["favorite_count"] + ["retweeted"] + ['hashtags'] + ['mention_screen_name'] + ['mention_name'] + ['mention_id'] + ['in_reply_to_user_id'] + ['in_reply_to_status_id']  + ['coordinates']  + ['quoted_status_id_str'] + ['reply_count'] + ['quote_count'] + ['language'])
            f.close()
        
        # query timeline for each handle
        if file_exists:
            f = open(self.datapath + outputfile, 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            for handle in handles.handles:
                tweets = api.user_timeline(screen_name=handle, count=100, include_rts=True)
                for tweet in tweets:
                    # print(tweet.text)
                    if len(tweet.entities['hashtags']) > 0:# get hashtags
                        if len(tweet.entities['user_mentions']) > 0:  # get user mention names
                            content = [[tweet.user.id_str, tweet.id_str, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorited, tweet.favorite_count, tweet.retweeted, tweet.entities['hashtags'][0]['text'], tweet.entities['user_mentions'][0]['screen_name'], tweet.entities['user_mentions'][0][ 'name'], tweet.entities['user_mentions'][0]['id'], tweet.in_reply_to_user_id_str, tweet.in_reply_to_status_id_str, tweet.lang]]

                            writer_top.writerows(content)
                    else:
                        content = [[tweet.user.id_str, tweet.id_str, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorited,tweet.favorite_count, tweet.retweeted, None, None, None, None, tweet.in_reply_to_user_id_str, tweet.in_reply_to_status_id_str, tweet.lang]]
                        writer_top.writerows(content)

            f.close()
            # gc.collect()
            return tweets


    def collect_user(self, handlesFile, outputfile):
        """Colect user profile"""

        # read handle list
        handles = self.___handles(handlesFile)

        # variable names
        file_exists = os.path.isfile(self.datapath + outputfile)

        if not file_exists:
            f = open(self.datapath + outputfile, 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer_top.writerow(["user_id"] + ["screen_name"] + ["location"] + ["user_description"] + ["followers_count"] + ["friends_count"] + ["account_created_at"] + ["favourites_count"] + ["statuses_count"] + ["user_url"] + ["listed_count"] + ["protected"] + ["verified"])
            f.close()

        # query user profile for each handle
        if file_exists:
            f = open(self.datapath + outputfile, 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            for handle in handles.handles:
                user = api.get_user(handle)
                content = [[user.id_str, user.screen_name, user.location, user.description, user.followers_count, user.friends_count, user.created_at, user.favourites_count, user.statuses_count, user.url, user.listed_count, user.protected, user.verified]]
                writer_top.writerows(content)
            f.close()
            gc.collect()

        return user

     


#tweet.id_str  tweet id


#load environment
evn_path = '/disk/data/share/s1690903/collect_tweets/environment/'
env = load_experiment(evn_path + 'env.yaml')

# query api
auth = tw.OAuthHandler(env['twitter_api']['consumer_key'], env['twitter_api']['consumer_secret'])
auth.set_access_token(env['twitter_api']['access_token'], env['twitter_api']['access_token_secret'])
api = tw.API(auth, wait_on_rate_limit=True)


collect = CollectTweets()
#tweets = collect.collect_tweets('handles.csv', 'tweets/test.csv')
Users = collect.collect_user('handles.csv', 'tweets/test_profile.csv')

# name = 'CAPYBARA_MAN'
# tweet_id = '1368145982958020000'
# # retrieved comments to the author
# comments = tw.Cursor(api.search, q='to:' + name, result_type='recent', timeout=999999).items(10000)

# replies = []
# for tweet in comments:
#     #print(tweet.in_reply_to_status_id_str)
#     if (tweet.in_reply_to_status_id_str == tweet_id):
#         print(tweet.text)
        #     replies.append(tweet)


# search tweets by words
# search_words = "#FridayFeeling"
# date_since = "2021-3-5"

# tweets = tw.Cursor(api.search,
#               q=search_words,
#               lang="en",
#               since=date_since).items(5)

# for tweet in tweets:
#     print(tweet.id_str)


