import pandas as pd
from newscatcherapi import NewsCatcherApiClient
import streamlit as st

st.header("Read the Latest/Breaking News")

# newscatcherapi = NewsCatcherApiClient(st.secrets["x_api_key"])
newscatcherapi = NewsCatcherApiClient(open("token.txt").read())

news_articles = newscatcherapi.get_search(q='*',
                                          from_="1 week ago",
                                          lang='en',
                                          # countries='SG',
                                          page_size=100)

col1, col2, col3 = st.columns(3)

# Industry
with col1:
    industry_option = st.selectbox(
        'Select Industries',
        ('Accounting', 'Venture Capital', 'Technology'))

# Technologies
with col2:
    technology_option = st.selectbox(
        'Select Technology',
        ('Cryptocurrency', 'CleanTech', 'Automation'))

# Type of Activity
with col3:
    activity_option = st.selectbox(
        'Select Activity',
        ('C Suite Hiring', 'Fundraising', 'Products', 'etc'))

col4, col5, col6 = st.columns(3)
with col4:
    competitor_option = st.selectbox(
        'Select Competitor of VPC',
        ('Geek+', 'Allay Therapeutics', 'Nium'))

with col5:
    customer_option = st.selectbox(
        'Select Customer of VPC',
        ('Geek+', 'Allay Therapeutics', 'Nium'))

with col6:
    geography_option = st.selectbox(
        'Select Geography',
        ('Singapore', 'Israel', 'US'))

context_option = st.text_input(
    'Define context of Search',
    'Show me data breaches from last 6 months')

api_articles = []

for article in news_articles["articles"]:
    temp_article = {"title": article["title"],
                    "link": article["link"],
                    "pub_date": article["published_date"],
                    "summary": article["excerpt"],
                    "image": article["media"],
                    "source": article["clean_url"],
                    "topic": article["topic"],
                    "country": article["country"],
                    "language": article["language"],
                    }
    api_articles.append(temp_article)

df = pd.DataFrame(api_articles)

col1, col2 = st.columns(2)
with col1:
    col1.metric("Count of Articles", len(df))
    article_count_df = (
        df.groupby("pub_date").count().reset_index()
    )
    # st.dataframe(df)
    st.bar_chart(article_count_df, x="pub_date", y="title")
with col2:
    col2.metric("Count of Sources", df["source"].nunique())
    sources_count_df = (
        df.groupby("source").count().reset_index()
    )

    # st.dataframe(sources_count_df)
    st.bar_chart(sources_count_df, x="source", y="title")

# columns = st.columns(2)
# no_of_articles = len(api_articles)
# article_index = 0
# col_index = -1


for index in range(len(api_articles)):
    article = api_articles[index]
    # with columns[0 if col_index < 0 else 1]:
    title = article["title"]
    link = article["link"]
    date = article["pub_date"]
    summary = article["summary"]
    source = article["source"]

    st.markdown(f"### [{title}]({link})")

    if article["image"]:
        st.image(article["image"])
    else:
        image = st.text("No Image")

    st.caption(f"Date: {date}")
    st.write(f"Source: {source}")
    st.write(f"Summary: {summary}")

    # if no_of_articles == article_index + 1:
    #     article_index += 1
    #     col_index *= -1
