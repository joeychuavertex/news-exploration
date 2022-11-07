import numpy as np
import streamlit as st
from newscatcherapi import NewsCatcherApiClient
import pandas as pd
from datetime import date


newscatcherapi = NewsCatcherApiClient(st.secrets["x_api_key"])


st.header("Analytics on Newscatcher")
st.write("To add count of articles")

vpcs = pd.read_excel("sample-vpc-list.xlsx")
vpc_companies = vpcs["Company/Service Name"].tolist()

query = st.selectbox("Companies", vpc_companies)

col1, col2 = st.columns(2)
with col1:
    from_date = st.date_input("Select Start Date", date(2020, 1, 1))
with col2:
    to_date = st.date_input("Select End Date", date.today())

news_articles = newscatcherapi.get_search(q=f"{query}",
                                          # from_="365 days ago",
                                          from_=str(from_date),
                                          to_=str(to_date),
                                          # lang='en',
                                          page_size=10
                                          )


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

