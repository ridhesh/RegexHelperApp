from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from .views import topHeadlines, publishedArticles
    app.add_url_rule('/', 'home', topHeadlines)
    app.add_url_rule('/published', 'published', publishedArticles)
    
    return app
