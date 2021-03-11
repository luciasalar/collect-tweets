import requests
import json
from ruamel import yaml
import gc
import csv
import os
import time
import pandas as pd
import time
import json


def load_experiment(path_to_experiment):
    """load experiment"""
    data = yaml.safe_load(open(path_to_experiment))
    return data

class CollectTweets:
    """Collect replies via twitter api v2."""

    def __init__(self, inputP, outputP, bearer_token, tweet_fields, query, until_id, outputFile):
        '''define the main path'''
        self.datapath = inputP# input path
        self.outputPath = outputP# output path
        #self.handlesFile = handlesFile
        self.bearer_token = bearer_token
        self.tweet_fields = tweet_fields
        self.query = query
        self.until_id = until_id
        self.outputFile = outputFile

    

    #search all allows 500 posts maximum
    def search_twitter(self):
        """Define search twitter function."""
        #curl "https://api.twitter.com/2/tweets/search/all?query=from%3Atwitterdev&max_results=500&start_time=2020-01-01T00%3A00%3A00Z&end_time=2020-03-31T11%3A59%3A59Z"

        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}

        url = "https://api.twitter.com/2/tweets/search/all?query={}&{}&max_results=500&until_id={}".format(
            self.query, self.tweet_fields, self.until_id)
        response = requests.request("GET", url, headers=headers)

        #print(response.status_code)

        if response.status_code != 200:
            time.sleep(60)
            #raise Exception(response.status_code, response.text)
        return response.json()



    def get_tweets(self):

        search_result = self.search_twitter()

       
        #'{}.csv'.format(self.outputFile)
        file_exists = os.path.isfile(self.outputPath + '{}.csv'.format(self.outputFile))

        if not file_exists:
            f = open(self.outputPath + '{}.csv'.format(self.outputFile), 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer_top.writerow(["text"] + ["author_id"] + ["created_at"] + ["conversation_id"] + ["tweet_id"] + ["retweet_count"] + ['reply_count'] + ['like_count'] + ['quote_count'] + ['in_reply_to_user_id'] + ["referenced_tweets_type"] + ["reference_tweet_id"])
            f.close()

        # query user profile for each handle
        if file_exists:
            with open(self.outputPath + '{}.json'.format(self.outputFile), 'a') as f:
                json.dump(search_result, f)

            f = open(self.outputPath + '{}.csv'.format(self.outputFile), 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            for tweet in search_result['data']: 
            #here I check whether in in_reply_to_user_id and referenced tweets are 
                if ('in_reply_to_user_id' in tweet.keys()) & ('referenced_tweets' not in tweet.keys()):
                     content = [[tweet['text'], tweet['author_id'], tweet['created_at'], tweet['conversation_id'], tweet['id'], tweet['public_metrics']['retweet_count'], tweet['public_metrics']['reply_count'], tweet['public_metrics']['like_count'], tweet['public_metrics']['quote_count'], tweet['in_reply_to_user_id'],  None, None]]

                elif ('in_reply_to_user_id' in tweet.keys()) & ('referenced_tweets' in tweet.keys()):
                    content = [[tweet['text'], tweet['author_id'], tweet['created_at'], tweet['conversation_id'], tweet['id'], tweet['public_metrics']['retweet_count'], tweet['public_metrics']['reply_count'], tweet['public_metrics']['like_count'], tweet['public_metrics']['quote_count'], tweet['in_reply_to_user_id'],  tweet['referenced_tweets'][0]['type'], tweet['referenced_tweets'][0]['id']]]


                elif ('in_reply_to_user_id' not in tweet.keys()) & ('referenced_tweets' in tweet.keys()):
                    content = [[tweet['text'], tweet['author_id'], tweet['created_at'], tweet['conversation_id'], tweet['id'], tweet['public_metrics']['retweet_count'], tweet['public_metrics']['reply_count'], tweet['public_metrics']['like_count'], tweet['public_metrics']['quote_count'], None,  tweet['referenced_tweets'][0]['type'], tweet['referenced_tweets'][0]['id']]]
              
                else:
                    content = [[tweet['text'], tweet['author_id'], tweet['created_at'], tweet['conversation_id'], tweet['id'], tweet['public_metrics']['retweet_count'], tweet['public_metrics']['reply_count'], tweet['public_metrics']['like_count'], tweet['public_metrics']['quote_count'], None, None, None]]
                writer_top.writerows(content)

            f.close()
            gc.collect()
        return search_result



class Loop_files:
    def __init__(self, datapath, outputPath, token, tweet_fields, handlesFile, outputFile):
        '''define the main path'''
        self.inputP = datapath# input path
        self.outputP = outputPath# output path
        self.handlesFile = handlesFile
        self.bearer_token = token
        self.tweet_fields = tweet_fields
        self.outputFile = outputFile
        #self.query = query
        # self.until_id = until_id

    def read_handles(self, handlesFile):
        """Read handle files"""

        handles = pd.read_csv(outputP + self.handlesFile)
        return handles


    def search_twitter_recent(self, bearer_token, query, tweet_fields):
        """Define search twitter function."""
        #curl "https://api.twitter.com/2/tweets/search/all?query=from%3Atwitterdev&max_results=500&start_time=2020-01-01T00%3A00%3A00Z&end_time=2020-03-31T11%3A59%3A59Z"

        headers = {"Authorization": "Bearer {}".format(self. bearer_token)}

        url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results=10".format(query, self.tweet_fields)
        response = requests.request("GET", url, headers=headers)

        print(response.status_code)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()


    def big_loop(self):
        handles = self.read_handles(self.handlesFile)

        for handle, status in zip(handles['screen_name'], handles['statuses_count']):
            # get handle name and pass it to query
            query = 'to:{}'.format(handle)

            #define how many loops, we don't know how many tweet reply this account has, so we get first 5000 replies
            loop_num = 1000

            #get the most recent 10 tweets of an account
            search_result = self.search_twitter_recent(self.bearer_token, query, self.tweet_fields)
            #You want to get the most recent post id as the until id
            until_id = search_result['data'][1]['id']
            # if handle=='eu_eeas':
            #     until_id = 707221617353617000

            # else:
            #     until_id = search_result['data'][1]['id']

            # here you can manually reset the id
            print(query, loop_num, until_id)
            time.sleep(5) #check rate limit to adjust this
            #https://developer.twitter.com/en/docs/twitter-api/rate-limits#v2-limits 
            

            # loop everything
        
            for i in range(1, loop_num + 1):
                print('this is the {} loop'.format(i))
                # collect tweets using query, for each loop, we get 500 tweets
                c = CollectTweets(inputP=self.inputP, outputP=self.outputP, bearer_token=self.bearer_token, tweet_fields=self.tweet_fields, query=query, until_id=until_id, outputFile=self.outputFile)
                #search_result = c.search_twitter()
                search_result = c.get_tweets()  #store result
                print('search id:', search_result['data'][-1]['id'])

                #set the new until_id as the last one on the list, next loop will continue up to this id
                new_until_id = search_result['data'][-1]['id']
                until_id = new_until_id

                time.sleep(5)#sleep 10s

                # except Exception:
                #     time.sleep(60)
                # if time.time() > timeout:
                #     time.sleep(20)
                #     timeout = time.time() + 60*2
               


evn_path = '/disk/data/share/s1690903/collect_tweets/environment/'
env = load_experiment(evn_path + 'env.yaml')


inputP = '/disk/data/share/s1690903/collect_tweets/data/'
outputP = '/disk/data/share/s1690903/collect_tweets/data/tweets/'
handles = 'handle_list_1.csv'
bearer_token = env['twitter_api']['bearer_token']
tweet_fields = "tweet.fields=text,author_id,created_at,conversation_id,in_reply_to_user_id,referenced_tweets,public_metrics"
handlesFile = 'handle_list_1.csv_profile.csv'
outputFile = 'recent_500000_comments'


lf = Loop_files(datapath=inputP, outputPath=outputP, token=bearer_token, tweet_fields=tweet_fields, handlesFile=handlesFile, outputFile=outputFile)
lf.big_loop()


# query = 'to:CAPYBARA_MAN'
# until_id = '1369786994033852417'
# c = CollectTweets(inputP=inputP, outputP=outputP, bearer_token=bearer_token, tweet_fields=tweet_fields, query=query, until_id=until_id, outputFile=outputFile)
#                     #search_result = c.search_twitter()
# search_result = c.get_tweets() 
# print(search_result['data'][0])















