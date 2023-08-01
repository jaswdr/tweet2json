import os
import json

import tweepy
import streamlit as st

st.set_page_config(page_title="Tweet2Json", page_icon=":bird:")
st.title("Tweet2Json")
st.write("""
Tweet2Json is a simple tool to get a tweet and its responses in JSON format.
""")

API_KEY = st.secrets.get("API_KEY", '')
API_KEY_SECRET = st.secrets.get("API_KEY_SECRET", '')

if not API_KEY or not API_KEY_SECRET:
    st.stop()

query_params = st.experimental_get_query_params()

with st.form(key="tweet2json"):
    tweet = st.text_input(
        "Enter a tweet ID or URL",
        value=query_params['tweet_id'][0] if 'tweet_id' in query_params else '',
        max_chars=255,
        help="Enter a tweet ID or URL to get the tweet and its responses in JSON format"
        )
    submitted = st.form_submit_button(label="Get JSON")

if submitted and tweet:
    # Get the tweet ID from tweet url
    if tweet.startswith("https://twitter.com/"):
        tweet_id = tweet.split("/")[-1]
    else:
        tweet_id = tweet

    # Get the tweet text, username, and date
    try:
        with st.spinner("Getting tweet..."):
            api = tweepy.API(tweepy.AppAuthHandler(API_KEY, API_KEY_SECRET))
            tweet = api.get_status(tweet_id)
            tweet_text = tweet.text
            tweet_username = tweet.user.screen_name
            tweet_date = tweet.created_at

            # Get the tweet responses
            tweet_responses = api.search_tweets(q="to:" + tweet_username, since_id=tweet_id, tweet_mode="extended")
            responses = []
            for response in tweet_responses:
                responses.append(response.__dict__['_json'])

            result = {
                "tweet": tweet.__dict__['_json'],
                "responses": responses
            }

            st.download_button(
                label="Download JSON",
                data=json.dumps(result),
                file_name="tweet2json.json",
                mime="application/json",
            )
            st.write(result)
    except Exception as e:
        st.error("Error: " + e.__str__())
else:
    st.info("Please enter a valid tweet ID or URL")

st.write("Made with ❤️ by [@jaswdr](https://twitter.com/jaswdr)")