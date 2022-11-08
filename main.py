from newscatcherapi import NewsCatcherApiClient
import streamlit as st

st.header("Read the Latest/Breaking News")

newscatcherapi = NewsCatcherApiClient(st.secrets["x_api_key"])

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
        ('C Suite Hiring', 'Fundraising', 'Others'))

col4, col5 = st.columns(2)
with col4:
    competitor_option = st.selectbox(
        'Select Competitor of VPC',
        ('Geek+', 'Allay Therapeutics', 'Nium'))

with col4:
    customer_option = st.selectbox(
        'Select Customer of VPC',
        ('Geek+', 'Allay Therapeutics', 'Nium'))



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


