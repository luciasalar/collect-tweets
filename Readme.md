# Collect Tweets

#Folders and Files

env: environment folders, keys, model parameters. These files are in local dir
data: tweet 

# Retrieve timeline

The new API has advanced functions in searching tweets, you might not need this function if you plan to collect all the tweets (up to 3200) of a user. We are currently using *API v1.1*

Twitter recenlty lauched API v.2, the new api enable you to search tweets in a more precise way. For example, You can set  start_time and end_time and paginating through the full results.
https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/introduction 

Unfortunately the library that are commonly used by many --Tweepy, doesn't support api2 yet. We can use scraping technqiues to do it, however, the tweepy library is way more convinient 


# Data dictionary v1.1
https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

### timeline object:
id_str: The string representation of the unique identifier for this Tweet.

text: tweets

created_at: tweet timestamp 

retweet_count: number of retweet

favorited: is the tweet being liked (boolean)

favorite_count: number of likes

retweeted: is the tweet being retweeted (boolean)

entities['hashtags'][0]['text']: hashtag

entities['user_mentions'][0]['screen_name']: mentioned account

entities['user_mentions'][0][ 'name']: mentioned account profile description

entities['user_mentions'][0]['id']: mentioned account id

in_reply_to_user_id_str: If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s author ID. This will not necessarily always be the user directly mentioned in the Tweet.

in_reply_to_status_id_str: If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s ID.

in_reply_to_screen_name: If the represented Tweet is a reply, this field will contain the screen name of the original Tweet’s author

lang: language

coordinates: Represents the geographic location of this Tweet as reported by the user or client application. 
place: When present, indicates that the tweet is associated (but not necessarily originating from) a Place 


### only available with the Premium and Enterprise tier products
quote_count: Indicates approximately how many times this Tweet has been quoted by Twitter users

reply_count: Number of times this Tweet has been replied to. Note: This object is only available with the Premium and Enterprise tier products. Note: This object is only available with the Premium and Enterprise tier products.

quoted_status_id_str: This field only surfaces when the Tweet is a quote Tweet. This field contains the integer value Tweet ID of the quoted Tweet. This field contains the integer value Tweet ID of the quoted Tweet. 


### User object
https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user

id_str: The string representation of the unique identifier for this User.

name: The name of the user, as they’ve defined it. Not necessarily a person’s name. Typically capped at 50 characters, but subject to change. 

screen_name: The screen name, handle, 

location: The user-defined location for this account’s profile. Not necessarily a location, nor machine-parseable. This field will occasionally be fuzzily interpreted by the Search service.

url: A URL provided by the user in association with their profile

description: The user-defined UTF-8 string describing their account.

verified: When true, indicates that the user has a verified account. 

followers_count:

friends_count: The number of users this account is following (AKA their “followings”).

listed_count: The number of public lists that this user is a member of.

favourites_count: The number of Tweets this user has liked in the account’s lifetime.

statuses_count: The number of Tweets (including retweets) issued by the user.

created_at: The UTC datetime that the user account was created on Twitter.

dervived: Provides the Profile Geo Enrichment metadata. {"locations": [{"country":"United States","country_code":"US","locality":"Denver"}]}

protected: When true, indicates that this user has chosen to protect their Tweets



