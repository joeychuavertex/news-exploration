from newscatcherapi import NewsCatcherApiClient
import streamlit as st

newscatcherapi = NewsCatcherApiClient(x_api_key='r5vce2FyTc1gog5rfMKkpbAcVNSS3vghqKSxEAzlcaQ')

news_articles = newscatcherapi.get_search(q='*',
                                          from_="1 week ago",
                                          lang='en',
                                          countries='CA',
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

    if article["image"] == None:
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

