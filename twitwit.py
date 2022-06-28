import tweepy
import wordcloud
import config
import json
import preprocessor as p
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
bearer_token = config.bearer_token
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=config.bearer_token)

new_stopwords = ['those', 'on', 'own', '’ve', 'yourselves', 'around', 'between', 'four', 'been', 'alone', 'off', 'am', 'then', 'other', 'can', 'regarding', 'hereafter', 'front', 'too', 'used', 'wherein', '‘ll', 'doing', 'everything', 'up', 'onto', 'never', 'either', 'how', 'before', 'anyway', 'since', 'through', 'amount', 'now', 'he', 'was', 'have', 'into', 'because', 'not', 'therefore', 'they', 'n’t', 'even', 'whom', 'it', 'see', 'somewhere', 'thereupon', 'nothing', 'whereas', 'much', 'whenever', 'seem', 'until', 'whereby', 'at', 'also', 'some', 'last', 'than', 'get', 'already', 'our', 'once', 'will', 'noone', "'m", 'that', 'what', 'thus', 'no', 'myself', 'out', 'next', 'whatever', 'although', 'though', 'which', 'would', 'therein', 'nor', 'somehow', 'whereupon', 'besides', 'whoever', 'ourselves', 'few', 'did', 'without', 'third', 'anything', 'twelve', 'against', 'while', 'twenty', 'if', 'however', 'herself', 'when', 'may', 'ours', 'six', 'done', 'seems', 'else', 'call', 'perhaps', 'had', 'nevertheless', 'where', 'otherwise', 'still', 'within', 'its', 'for', 'together', 'elsewhere', 'throughout', 'of', 'others', 'show', '’s', 'anywhere', 'anyhow', 'as', 'are', 'the', 'hence', 'something', 'hereby', 'nowhere', 'latterly', 'say', 'does', 'neither', 'his', 'go', 'forty', 'put', 'their', 'by', 'namely', 'could', 'five', 'unless', 'itself', 'is', 'nine', 'whereafter', 'down', 'bottom', 'thereby', 'such', 'both', 'she', 'become', 'whole', 'who', 'yourself', 'every', 'thru', 'except', 'very', 'several', 'among', 'being', 'be', 'mine', 'further', 'n‘t', 'here', 'during', 'why', 'with', 'just', "'s", 'becomes', '’ll', 'about', 'a', 'using', 'seeming', "'d", "'ll", "'re", 'due', 'wherever', 'beforehand', 'fifty', 'becoming', 'might', 'amongst', 'my', 'empty', 'thence', 'thereafter', 'almost', 'least', 'someone', 'often', 'from', 'keep', 'him', 'or', '‘m', 'top', 'her', 'nobody', 'sometime', 'across', '‘s', '’re', 'hundred', 'only', 'via', 'name', 'eight', 'three', 'back', 'to', 'all', 'became', 'move', 'me', 'we', 'formerly', 'so', 'i', 'whence', 'under', 'always', 'himself', 'in', 'herein', 'more', 'after', 'themselves', 'you', 'above', 'sixty', 'them', 'your', 'made', 'indeed', 'most', 'everywhere', 'fifteen', 'but', 'must', 'along', 'beside', 'hers', 'side', 'former', 'anyone', 'full', 'has', 'yours', 'whose', 'behind', 'please', 'ten', 'seemed', 'sometimes', 'should', 'over', 'take', 'each', 'same', 'rather', 'really', 'latter', 'and', 'ca', 'hereupon', 'part', 'per', 'eleven', 'ever', '‘re', 'enough', "n't", 'again', '‘d', 'us', 'yet', 'moreover', 'mostly', 'one', 'meanwhile', 'whither', 'there', 'toward', '’m', "'ve", '’d', 'give', 'do', 'an', 'quite', 'these', 'everyone', 'towards', 'this', 'cannot', 'afterwards', 'beyond', 'make', 'were', 'whether', 'well', 'another', 'below', 'first', 'upon', 'any', 'none', 'many', 'serious', 'various', 're', 'two', 'less', '‘ve', 'moleg', 'thank', 'missouri', 'im']

stpwrd = nltk.corpus.stopwords.words('english')
stpwrd.extend(new_stopwords)          

class twitwit:

    def __init__(self):      

        return
    
    def _makeitastring(self, wannabestring):
        
        clean_words = []
        final_clean_words = []
        
        convertedstring = ','.join(map(str, wannabestring))
        re.sub(' +', ' ', convertedstring)
        convertedstring = convertedstring.replace(',,', ' ')
        convertedstring = convertedstring.replace(',', ' ')
        convertedstring = convertedstring.replace('  ', ' ')
        text_tokens = word_tokenize(convertedstring)  

        for w in text_tokens:
            if w not in stpwrd:
                final_clean_words.append(w)

        
        return final_clean_words 
    
    def stringIT(self, wannabestring):
        convertedstring = ','.join(map(str, wannabestring))
        return(convertedstring)


    def getTwitterID(self, username):

        response = client.get_user(username=username)
        userID = response.data.id

        return userID

    def getFollowersCount(self, username):

        response = client.get_user(username=username, user_fields=["created_at", "description", "entities", "id", "location",
                                   "name,pinned_tweet_id", "profile_image_url", "public_metrics", "url", "username", "verified", "withheld"], expansions=["pinned_tweet_id"])

        followersCount = response.data.public_metrics.get("followers_count")

        return followersCount

    def getCleanTweetWords(self, userID):
        
        p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.EMOJI, p.OPT.SMILEY)
        clean_tweet_word_list = []
        # response = client.get_users_tweets(id=userID, max_results=100)
        response = tweepy.Paginator(client.get_users_tweets, id=userID, max_results=100).flatten(limit=150)
        
        for tweet in response:
            if not tweet.text.startswith('RT'):
                clean_tweet = tweet.text                
                clean_tweet = p.clean(tweet.text)
                final_clean_tweet =  "".join([char for char in clean_tweet if char not in string.punctuation])  
                final_clean_tweet = final_clean_tweet.lower()       
                clean_tweet_word_list.append(final_clean_tweet)
                word_list = self._makeitastring(clean_tweet_word_list)

        return word_list
    
    def black_color_func(self, word, font_size, position,orientation,random_state=None, **kwargs):
        return("hsl(0,100%, 1%)")
    
    def getWordCloud(self, data):
        wordcloud = WordCloud(font_path="AllerDisplay.ttf", background_color="white", width=3000, height=2000, max_words=350).generate_from_text(data)
        # set the word color to black
        wordcloud.recolor(color_func = self.black_color_func)
        wordcloud.width = 3000
        wordcloud.height = 2000
        plt.axis("off")
        plt.imshow(wordcloud)
        plt.savefig('wordcloud.png', dpi=200)
       
        return
        
        
t = twitwit()

tweets = t.getCleanTweetWords(t.getTwitterID("bobondermo"))

str_tweets = t.stringIT(tweets)

t.getWordCloud(str_tweets)





# data = pd.DataFrame(tweets)

# data.rename(columns = {0:'words'}, inplace = True)

# t.getWordCloud(tweets)







