import streamlit as st
import twitwit
import time

t = twitwit.twitwit()

st.title("Twitter Utilities")
st.set_option('deprecation.showPyplotGlobalUse', False)

selection_list = ["Twitter User Information", "Twitter User Wordcloud by Tweets", "Twitter User Wordcloud by Likes"]
st.sidebar.title("Select Twitter Tool")
selection = st.sidebar.selectbox(label = "", options = selection_list)

if selection == "Twitter User Information":
    st.header("Get Twitter User Information")
    twitter_name = st.text_input(
        "Enter Twitter Screen Name to Get Information about Twitter User:"
        )
    if twitter_name:
        user_info = t.get_user_information(twitter_name)
        st.image(user_info['user_image_url'])
        st.write("Link to Twitter User Profile: ", user_info['user_profile_link'])
        st.write("Twitter Screen Name: ", f"@{user_info['screen_name']}")
        st.write("Twitter User Name: ", user_info['user_name'])
        st.write("Twitter User ID ", user_info['user_twitter_id'])
        st.write("Twitter User Created on: ", user_info['user_created_at'])
        st.write("Twitter User Verified Status: ", user_info['user_verified'])
        st.write("Twitter User Description: ", user_info['user_description'])
        st.write("Twitter User # of Tweets: ", user_info['user_tweets'])
        st.write("Twitter User # of Liked Tweets: ", user_info['user_liked_tweets'])
        st.write("Twitter User Followers: ", user_info['user_following_count'])
        st.write("Twitter User Following ", user_info['user_followers_count'])
        st.write("Twitter Geo Enabled: ", user_info['user_get_enabled'])
        st.write("Twitter User List Membershops: ", user_info['user_listed_count'])
        
elif selection == "Twitter User Wordcloud by Tweets":
    st.header("Get Twitter User Wordcloud From Their Recent Tweets")
    twitter_name = st.text_input(
        "Enter Twitter screen name to get wordcloud of user's recent tweets")
    if twitter_name:  
            st.write("This may take up to 60 seconds but it is worth it!") 
            st.write("Getting user's recent tweets...")
            title = f"Latest tweets by @{twitter_name}. #moleg brought to you by @politwit1984"
            tweets = t.getUserTweets(t.getTwitterID(twitter_name))
            st.write("Cleaning user's tweets...")
            washed_tweets = t.washTweetsForCloud(tweets)
            st.write("Generating wordcloud - this is the long part...")
            str_tweets = t.stringIT(washed_tweets)
            t.getWordCloud(str_tweets, title, "like")
            st.pyplot()
            st.write("We told you that you'd like it!")
            st.write("Right click on the image to save and tweet it out.")
            st.write("If you want to getanotherwordcloud, just enter a new name above.")
            
elif selection == "Twitter User Wordcloud by Likes":
    st.header("Get Twitter User Wordcloud From Tweets They've Recently Liked")
    twitter_name = st.text_input(
        "Enter Twitter screen name to get wordcloud of user's recent liked tweets")
    if twitter_name:  
            st.write("This may take up to 60 seconds but it is worth it!") 
            st.write("Getting user's recent tweets...")
            title = f"Tweets liked by @{twitter_name}. #moleg brought to you by @politwit1984"
            tweets = t.getUserLikedTweets(t.getTwitterID(twitter_name))
            st.write("Cleaning user's tweets...")
            washed_tweets = t.washTweetsForCloud(tweets)
            st.write("Generating wordcloud - this is the long part...")
            st.write("While you are waiting, this is my favorite wordcloud. Many users don't post what they really think but will like tweets that they agree with. This is a great way to get a sense of what people are thinking.")
            str_tweets = t.stringIT(washed_tweets)
            t.getWordCloud(str_tweets, title, "likes")
            st.pyplot()
            st.write("We told you that you'd like it!")
            st.write("Right click on the image to save and tweet it out.")
            st.write("If you want to getanotherwordcloud, just enter a new name above.")
                

