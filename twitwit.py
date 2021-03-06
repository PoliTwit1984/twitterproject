import re
import string

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import preprocessor as p
import tweepy
import wordcloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image
from wordcloud import WordCloud
from collections import Counter



import config

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
bearer_token = config.bearer_token
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=config.bearer_token)

new_stopwords = [
    "those",
    "on",
    "own",
    "’ve",
    "yourselves",
    "around",
    "between",
    "four",
    "been",
    "alone",
    "off",
    "am",
    "then",
    "other",
    "can",
    "regarding",
    "hereafter",
    "front",
    "too",
    "used",
    "wherein",
    "‘ll",
    "doing",
    "everything",
    "up",
    "onto",
    "never",
    "either",
    "how",
    "before",
    "anyway",
    "since",
    "through",
    "amount",
    "now",
    "he",
    "was",
    "have",
    "into",
    "because",
    "not",
    "therefore",
    "they",
    "n’t",
    "even",
    "whom",
    "it",
    "see",
    "somewhere",
    "thereupon",
    "nothing",
    "whereas",
    "much",
    "whenever",
    "seem",
    "until",
    "whereby",
    "at",
    "also",
    "some",
    "last",
    "than",
    "get",
    "already",
    "our",
    "once",
    "will",
    "noone",
    "'m",
    "that",
    "what",
    "thus",
    "no",
    "myself",
    "out",
    "next",
    "whatever",
    "although",
    "though",
    "which",
    "would",
    "therein",
    "nor",
    "somehow",
    "whereupon",
    "besides",
    "whoever",
    "ourselves",
    "few",
    "did",
    "without",
    "third",
    "anything",
    "twelve",
    "against",
    "while",
    "twenty",
    "if",
    "however",
    "herself",
    "when",
    "may",
    "ours",
    "six",
    "done",
    "seems",
    "else",
    "call",
    "perhaps",
    "had",
    "nevertheless",
    "where",
    "otherwise",
    "still",
    "within",
    "its",
    "for",
    "together",
    "elsewhere",
    "throughout",
    "of",
    "others",
    "show",
    "’s",
    "anywhere",
    "anyhow",
    "as",
    "are",
    "the",
    "hence",
    "something",
    "hereby",
    "nowhere",
    "latterly",
    "say",
    "does",
    "neither",
    "his",
    "go",
    "forty",
    "put",
    "their",
    "by",
    "namely",
    "could",
    "five",
    "unless",
    "itself",
    "is",
    "nine",
    "whereafter",
    "down",
    "bottom",
    "thereby",
    "such",
    "both",
    "she",
    "become",
    "whole",
    "who",
    "yourself",
    "every",
    "thru",
    "except",
    "very",
    "several",
    "among",
    "being",
    "be",
    "mine",
    "further",
    "n‘t",
    "here",
    "during",
    "why",
    "with",
    "just",
    "'s",
    "becomes",
    "’ll",
    "about",
    "a",
    "using",
    "seeming",
    "'d",
    "'ll",
    "'re",
    "due",
    "wherever",
    "beforehand",
    "fifty",
    "becoming",
    "might",
    "amongst",
    "my",
    "empty",
    "thence",
    "thereafter",
    "almost",
    "least",
    "someone",
    "often",
    "from",
    "keep",
    "him",
    "or",
    "‘m",
    "top",
    "her",
    "nobody",
    "sometime",
    "across",
    "‘s",
    "’re",
    "hundred",
    "only",
    "via",
    "name",
    "eight",
    "three",
    "back",
    "to",
    "all",
    "became",
    "move",
    "me",
    "we",
    "formerly",
    "so",
    "i",
    "whence",
    "under",
    "always",
    "himself",
    "in",
    "herein",
    "more",
    "after",
    "themselves",
    "you",
    "above",
    "sixty",
    "them",
    "your",
    "made",
    "indeed",
    "most",
    "everywhere",
    "fifteen",
    "but",
    "must",
    "along",
    "beside",
    "hers",
    "side",
    "former",
    "anyone",
    "full",
    "has",
    "yours",
    "whose",
    "behind",
    "please",
    "ten",
    "seemed",
    "sometimes",
    "should",
    "over",
    "take",
    "each",
    "same",
    "rather",
    "really",
    "latter",
    "and",
    "ca",
    "hereupon",
    "part",
    "per",
    "eleven",
    "ever",
    "‘re",
    "enough",
    "n't",
    "again",
    "‘d",
    "us",
    "yet",
    "moreover",
    "mostly",
    "one",
    "meanwhile",
    "whither",
    "there",
    "toward",
    "’m",
    "'ve",
    "’d",
    "give",
    "do",
    "an",
    "quite",
    "these",
    "everyone",
    "towards",
    "this",
    "cannot",
    "afterwards",
    "beyond",
    "make",
    "were",
    "whether",
    "well",
    "another",
    "below",
    "first",
    "upon",
    "any",
    "none",
    "many",
    "serious",
    "various",
    "re",
    "two",
    "less",
    "‘ve",
    "moleg",
    "thank",
    "missouri",
    "im",
    "hes",
    "amp",
    "ive",
    "cant",
    "dont",
    "mosen"
]

stpwrd = nltk.corpus.stopwords.words("english")
stpwrd.extend(new_stopwords)


class twitwit:
    def __init__(self):

        return

    def stringIT(self, wannabestring):
        convertedstring = ",".join(map(str, wannabestring))
        return convertedstring

    def getFollowedList(self, user_id):
        response = client.get_followed_lists(id=user_id)
        return response

    def getTwitterID(self, username):
        response = client.get_user(username=username)
        user_id = response.data.id
        return user_id

    def getFollowersCount(self, username):
        """
        It gets the followers count of a user.
        
        :param username: The username of the account you want to get the followers count of
        :return: The followers count of the user.
        """
        response = client.get_user(
            username=username,
            user_fields=[
                "created_at",
                "description",
                "entities",
                "id",
                "location",
                "name,pinned_tweet_id",
                "profile_image_url",
                "public_metrics",
                "url",
                "username",
                "verified",
                "withheld",
            ],
            expansions=["pinned_tweet_id"],
        )
        followersCount = response.data.public_metrics.get("followers_count")
        return followersCount

    def washTweetsForCloud(self, response):
       # Cleaning the tweets and removing punctuation, stopwords, and other things.
        p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.EMOJI, p.OPT.SMILEY)
        clean_tweet_word_list = []
        final_clean_words = []
        for tweet in response:
            if not tweet.text.startswith("RT"):
                clean_tweet = tweet.text
                clean_tweet = p.clean(tweet.text)
                final_clean_tweet = "".join(
                    [char for char in clean_tweet if char not in string.punctuation]
                )
                final_clean_tweet = final_clean_tweet.lower()
                clean_tweet_word_list.append(final_clean_tweet)

        convertedstring = ",".join(map(str, clean_tweet_word_list))
        re.sub(" +", " ", convertedstring)
        convertedstring = convertedstring.replace(",,", " ")
        convertedstring = convertedstring.replace(",", " ")
        convertedstring = convertedstring.replace("  ", " ")
        text_tokens = word_tokenize(convertedstring)

        for w in text_tokens:
            if w not in stpwrd:
                final_clean_words.append(w)

        return final_clean_words

    def getUserTweets(self, user_id):
        """
        It gets the tweets of a user.
        
        :param user_id: The user ID of the user you want to get tweets from
        :return: A list of tweets
        """

        response = tweepy.Paginator(
            client.get_users_tweets, id=user_id, max_results=100
        ).flatten(limit=150)

        return response

    def getUserLikedTweets(self, user_id):

        response = tweepy.Paginator(
            client.get_liked_tweets, id=user_id, max_results=100
        ).flatten(limit=150)

        return response

    def _black_color_func(
        self, word, font_size, position, orientation, random_state=None, **kwargs
    ):
        return "hsl(0,100%, 1%)"

    def getWordCloud(self, data, title, mask):
        if mask == "likes":
            img_mask = np.array(Image.open("heart.png"))
            location = "center"
        else:
            img_mask = np.array(Image.open("heart.png"))
            location = "center"

        title_font = {"family": "MV Boli", "color": "black", "size": 20}

        wordcloud = WordCloud(
            font_path="AllerDisplay.ttf",
            background_color="white",
            width=3000,
            height=2000,
            mask=img_mask,
            max_words=500,
        ).generate_from_text(data)
        wordcloud.recolor(color_func=self._black_color_func)
        plt.figure(figsize=(15, 10))
        plt.title(title, fontdict=title_font, loc=location)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        plt.savefig("words.png")

        return

    def get_user_information(self, twitter_user):

        dict = {}
        user = api.get_user(screen_name=twitter_user)
        dict["screen_name"] = user.screen_name
        dict["user_name"] = user.name
        dict["user_description"] = user.description
        dict["user_location"] = user.location
        dict["user_created_at"] = user.created_at
        dict["user_tweets"] = user.statuses_count
        dict["user_liked_tweets"] = user.favourites_count
        dict["user_followers_count"] = user.friends_count
        dict["user_following_count"] = user.followers_count
        dict["user_get_enabled"] = user.geo_enabled
        dict["user_twitter_id"] = user.id
        dict["user_listed_count"] = user.listed_count
        dict["user_verified"] = user.verified
        dict["user_geo_enabled"] = user.geo_enabled
        dict["user_profile_link"] = "https://twitter.com/" + user.screen_name
        dict["user_created_at"] = user.created_at
        dict["user_image_url"] = user.profile_image_url

        return dict

    def get_twitter_trends(self):
        trend_list = []
        response = api.get_place_trends("2486982")  # WOEID for St. Louis, MO
        
        for i in response:
            for key in i.keys():
                if key == "trends":
                    for trend in i[key]:
                        trend_list.append(trend["name"])

        return trend_list
    
    def get_user_list_membership(self, user_id):
        response = client.get_list_memberships(id=user_id) 
        for membership in response:
            print(membership.name)
        return response
    
    def get_trending_words(self):
        query = "#moleg #mosen -is:retweet"
        response = client.search_recent_tweets(query=query, max_results=100)        
        tweet_list = self.washTweetsForCloud(response)        
        word_count = Counter(tweet_list)   

        return word_count
    
t = twitwit()

word_count = t.get_trending_words()

print(word_count)




        

        
        



