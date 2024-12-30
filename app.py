import streamlit as st
import requests
from datetime import datetime, timedelta

# API Configuration
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'
TOP_NEWS_ENDPOINT = 'https://newsapi.org/v2/top-headlines'
NEWS_API_KEY = '3ca4fa08040e483ca5011b0e67efd0ad'

# Helper function to display articles (moved to top)
def display_article(article):
    col1, col2 = st.columns([1, 2])
    with col1:
        if article.get('urlToImage'):
            st.image(article['urlToImage'], use_container_width=True)
    with col2:
        st.markdown(
            f"""
            <h3><a href="{article['url']}" class="news-title" target="_blank">{article['title']}</a></h3>
            <p><span class="news-source"><strong>Source:</strong> {article.get('source', {}).get('name', 'Unknown')}</span></p>
            <p><span class="news-date"><strong>Published:</strong> {article.get('publishedAt', 'Unknown date')[:10]}</span></p>
            <p>{article.get('description', 'No description available')}</p>
            """,
            unsafe_allow_html=True
        )
    st.markdown("<hr>", unsafe_allow_html=True)

def fetch_top_headlines(country='us', category=None, pageSize=6):
    params = {
        'apiKey': NEWS_API_KEY,
        'country': country,
        'pageSize': pageSize
    }
    if category:
        params['category'] = category
    response = requests.get(TOP_NEWS_ENDPOINT, params=params)
    return response.json()

def fetch_news(query=None, language='en', sort_by='publishedAt', pageSize=100):
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    params = {
        'apiKey': NEWS_API_KEY,
        'language': language,
        'from': from_date,
        'sortBy': sort_by,
        'pageSize': pageSize
    }
    if query:
        params['q'] = query
    response = requests.get(NEWS_API_ENDPOINT, params=params)
    return response.json()

# Page configuration
st.set_page_config(page_title='Advanced News Aggregator', layout='wide')
st.title('Advanced News Aggregator')

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1585241645927-c7a8e5840c42?ixlib=rb-4.0.3");
        background-attachment: fixed;
        background-size: cover;
    }
    .news-title { color: #1E88E5; text-decoration: none; }
    .news-source { color: #4CAF50; }
    .news-date { color: #9E9E9E; }
    .section-header {
        background-color: rgba(0,0,0,0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.header('Search Options')
    search_query = st.text_input('Search for news', '')
    
    languages = {
        'English': 'en',
        'Arabic': 'ar',
        'German': 'de',
        'Spanish': 'es',
        'French': 'fr',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Russian': 'ru'
    }
    selected_language = st.selectbox('Select Language', list(languages.keys()))
    
    sort_options = {
        'Most Recent': 'publishedAt',
        'Most Relevant': 'relevancy',
        'Most Popular': 'popularity'
    }
    selected_sort = st.selectbox('Sort By', list(sort_options.keys()))
    
    st.markdown("---")
    if st.button('Refresh News'):
        st.rerun()
    st.markdown("Page will automatically refresh every 5 minutes.")

# Display logic
if search_query:
    # Search results
    news = fetch_news(
        query=search_query,
        language=languages[selected_language],
        sort_by=sort_options[selected_sort]
    )
    if 'articles' in news:
        st.markdown("<div class='section-header'><h2>Search Results</h2></div>", unsafe_allow_html=True)
        for article in news['articles']:
            display_article(article)
else:
    # Homepage content
    # Top Headlines
    top_news = fetch_top_headlines(pageSize=6)
    if 'articles' in top_news:
        st.markdown("<div class='section-header'><h2>Breaking News</h2></div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, article in enumerate(top_news['articles'][:6]):
            with cols[idx % 3]:
                if article.get('urlToImage'):
                    st.image(article['urlToImage'], use_container_width=True)
                st.markdown(f"<h4><a href='{article['url']}' target='_blank' class='news-title'>{article['title']}</a></h4>", unsafe_allow_html=True)
    
    # Popular News
    popular_news = fetch_news(sort_by='popularity', pageSize=6)
    if 'articles' in popular_news:
        st.markdown("<div class='section-header'><h2>Trending Stories</h2></div>", unsafe_allow_html=True)
        for article in popular_news['articles']:
            col1, col2 = st.columns([1, 2])
            with col1:
                if article.get('urlToImage'):
                    st.image(article['urlToImage'], use_container_width=True)
            with col2:
                st.markdown(
                    f"""
                    <h3><a href="{article['url']}" class="news-title" target="_blank">{article['title']}</a></h3>
                    <p><span class="news-source"><strong>Source:</strong> {article.get('source', {}).get('name', 'Unknown')}</span></p>
                    <p><span class="news-date"><strong>Published:</strong> {article.get('publishedAt', 'Unknown date')[:10]}</span></p>
                    <p>{article.get('description', 'No description available')}</p>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown("<hr>", unsafe_allow_html=True)

# Auto-refresh
st.markdown(
    """
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 300000);
    </script>
    """,
    unsafe_allow_html=True
)
  
