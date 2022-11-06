from datetime import date
import pandas as pd
import streamlit as st
from newscatcherapi import NewsCatcherApiClient

newscatcherapi = NewsCatcherApiClient(st.secrets["x_api_key"])

st.header("Search VPC News")

vpcs = pd.read_excel("sample-vpc-list.xlsx")
vpc_companies = vpcs["Company/Service Name"].tolist()

query = st.selectbox("Companies", vpc_companies)
add_query = st.text_input("Add Keywords", "allay")
suggested_keywords_add = st.caption("Add: allay")
not_query = st.text_input("Remove Keywords", "singapore", placeholder="Type Keywords to Remove")
suggested_keywords_remove = st.caption("Suggestions: singapore")


col1, col2 = st.columns(2)
with col1:
    from_date = st.date_input("Select Start Date", date(2020, 1, 1))
with col2:
    to_date = st.date_input("Select End Date", date.today())

news_articles = newscatcherapi.get_search(q=f"{query} AND {add_query} NOT {not_query}",
                                          # from_="365 days ago",
                                          from_=str(from_date),
                                          to_=str(to_date),
                                          lang='en',
                                          page_size=10)

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

    if article["image"] is None:
        image = st.text("No Image")
    else:
        image = article["image"]
        st.image(image)

    st.caption(f"Date: {date}")
    st.write(f"Source: {source}")
    st.write(f"Summary: {summary}")

    # if no_of_articles == article_index + 1:
    #     article_index += 1
    #     col_index *= -1
