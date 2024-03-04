import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV files
cluster_df = pd.read_csv("C:\\Users\\2211592\\Downloads\\cluster_for_110_topics.csv")
topic_df = pd.read_csv("C:\\Users\\2211592\\OneDrive - Cognizant\\Desktop\\gen ai\\topic_name_110_Final 2.csv")

# Read the Excel file with tweets data
excel_file = "C:\\Users\\2211592\\OneDrive - Cognizant\\Desktop\\gen ai\\tweets_with_sentiment.xlsx"
excel_data = pd.read_excel(excel_file, sheet_name=None)

# Function to filter tweets data based on selected topic and sentiment
def filter_tweets(topic_id, sentiment_label):
    tweets = excel_data[f"Topic_{topic_id}"]
    filtered_tweets = tweets[tweets['sentiment_label'] == sentiment_label]
    return filtered_tweets

# Streamlit app
st.title("Tweet Sentiment Analysis")

# Dropdown menu for selecting the cluster
selected_cluster = st.selectbox("Select a cluster", [''] + list(cluster_df.columns))

if selected_cluster:
    # Filter topics based on selected cluster
    topics_in_cluster = cluster_df[selected_cluster].dropna().tolist()

    # Dropdown menu for selecting the topic
    selected_topic = st.selectbox("Select a topic", [''] + topics_in_cluster)

    if selected_topic:
        # Get topic ID based on selected topic name
        topic_id = topic_df[topic_df['Topic_Name'] == selected_topic]['Topic'].values[0]

        # Display tweet count for selected topic
        topic_count = topic_df[topic_df['Topic'] == topic_id]['Count'].values[0]
        st.write(f"Number of tweets under {selected_topic}: {topic_count}")

        # Display sentiment analysis bar chart
        sentiments = ['positive', 'negative', 'neutral']
        sentiment_counts = []
        for sentiment in sentiments:
            filtered_tweets = filter_tweets(topic_id, sentiment)
            sentiment_counts.append(len(filtered_tweets))

        # Create a color dictionary for the bar chart
        color_dict = {'positive': 'red', 'negative': 'blue', 'neutral': 'green'}

        # Plot the bar chart
        fig, ax = plt.subplots(figsize=(8, 3))
        sns.barplot(x=sentiments, y=sentiment_counts, palette=[color_dict[sentiment] for sentiment in sentiments], ax=ax)
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        st.pyplot(fig)

        # Display count of tweets for each sentiment category
        st.write("Count of tweets by sentiment category:")
        for sentiment, count in zip(sentiments, sentiment_counts):
            st.write(f"{sentiment.capitalize()}: {count}")

        # Display sample tweets for each sentiment category
        for sentiment in sentiments:
            st.subheader(f"Sample tweets for {sentiment} sentiment:")
            filtered_tweets = filter_tweets(topic_id, sentiment)
            sample_tweets = filtered_tweets.sample(min(5, len(filtered_tweets)))
            # Convert tweet_id to string to avoid error sign
            sample_tweets['tweet_id'] = sample_tweets['tweet_id'].astype(str)
            st.write(sample_tweets[['tweet_id', 'text']])

        # Add option to download all tweets under the topic in CSV format
        if st.button("Download all tweets under this topic"):
            filtered_tweets = excel_data[f"Topic_{topic_id}"]
            # Convert tweet_id to string to avoid error when downloading CSV
            filtered_tweets['tweet_id'] = filtered_tweets['tweet_id'].astype(str)
            csv_data = filtered_tweets.to_csv(index=False)
            st.download_button(label="Click to download", data=csv_data, file_name=f"{selected_topic}_tweets.csv", mime='text/csv')