from newsapi import NewsApiClient
from config import Config
from models import Articles

def fetch_articles(source_list):
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    articles_data = newsapi.get_everything(sources=source_list)
    all_articles = articles_data['articles']
    articles_results = []

    for article in all_articles:
        article_object = Articles(
            source=article['source']['name'],
            title=article['title'],
            desc=article['description'],
            author=article['author'],
            img=article['urlToImage'],
            p_date=article['publishedAt'],
            url=article['url']
        )
        articles_results.append(article_object)

    return articles_results

def topHeadlines():
    return fetch_articles('cnn, reuters, cnbc, techcrunch, the-verge, gizmodo, the-next-web, techradar, recode, ars-technica')

def publishedArticles():
    return fetch_articles('cnn, reuters, cnbc, the-verge, gizmodo, the-next-web, techradar, recode, ars-technica')

def randomArticles():
    return fetch_articles('the-verge, gizmodo, the-next-web, recode, ars-technica')

def businessArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    business_articles = newsapi.get_top_headlines(category='business')
    all_articles = business_articles['articles']
    articles_results = []

    for article in all_articles:
        article_object = Articles(
            source=article['source']['name'],
            title=article['title'],
            desc=article['description'],
            author=article['author'],
            img=article['urlToImage'],
            p_date=article['publishedAt'],
            url=article['url']
        )
        articles_results.append(article_object)

    return articles_results

def techArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    tech_articles = newsapi.get_top_headlines(category='technology')
    all_articles = tech_articles['articles']
    articles_results = []

    for article in all_articles:
        article_object = Articles(
            source=article['source']['name'],
            title=article['title'],
            desc=article['description'],
            author=article['author'],
            img=article['urlToImage'],
            p_date=article['publishedAt'],
            url=article['url']
        )
        articles_results.append(article_object)

    return articles_results

def entArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    ent_articles = newsapi.get_top_headlines(category='entertainment')
    all_articles = ent_articles['articles']
    articles_results = []

    for article in all_articles:
        article_object = Articles(
            source=article['source']['name'],
            title=article['title'],
            desc=article['description'],
            author=article['author'],
            img=article['urlToImage'],
            p_date=article['publishedAt'],
            url=article['url']
        )
        articles_results.append(article_object)

    return articles_results

def scienceArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    science_articles = newsapi.get_top_headlines(category='science')
    all_articles = science_articles['articles']
    articles_results = []

    for article in all_articles:
        article_object = Articles(
            source=article['source']['name'],
            title=article['title'],
            desc=article['description'],
            author=article['author'],
            img=article['urlToImage'],
            p_date=article['publishedAt'],
            url=article['url']
        )
        articles_results.append(article_object)

    return articles_results

def sportArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    sport_articles = newsapi.get_top_headlines(category='sports')
    all_articles = sport_articles['articles']
    articles_results = []

    for article in all_articles:
        article_object = Articles(
            source=article['source']['name'],
            title=article['title'],
            desc=article['description'],
            author=article['author'],
            img=article['urlToImage'],
            p_date=article['publishedAt'],
            url=article['url']
        )
        articles_results.append(article_object)

    return articles_results

def healthArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    health_articles = newsapi.get_top_headlines(category='health')
    all_articles = health_articles['articles']
    articles_results = []

    for article in all_articles:
        article_object = Articles(
            source=article['source']['name'],
            title= article['title'],
            desc=article['description'],
            author=article['author'],
            img=article['urlToImage'],
            p_date=article['publishedAt'],
            url=article['url']
        )
        articles_results.append(article_object)

    return articles_results