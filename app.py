import twitwit
import streamlit as st

t = twitwit.twitwit()

id = t.convertUserNameToID(username="dingersandks")
followers_count = t.getFollowersCount(username="dingersandks")

st.title(id)
st.title(followers_count)



