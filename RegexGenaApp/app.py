from flask import Flask, render_template
from news_fetcher import topHeadlines, publishedArticles, randomArticles, businessArticles, techArticles, entArticles, scienceArticles, sportArticles, healthArticles

app = Flask(__name__)

@app.route('/')
def index():
    articles = topHeadlines()
    return render_template('index.html', articles=articles)

@app.route('/published')
def published():
    articles = publishedArticles()
    return render_template('articles.html', articles=articles, title="Published Articles")

@app.route('/random')
def random():
    articles = randomArticles()
    return render_template('random_articles.html', articles=articles, title="Random Articles")

@app.route('/business')
def business():
    articles = businessArticles()
    return render_template('business_articles.html', articles=articles, title="Business Articles")

@app.route('/tech')
def tech():
    articles = techArticles()
    return render_template('tech_articles.html', articles=articles, title="Technology Articles")

@app.route('/entertainment')
def entertainment():
    articles = entArticles()
    return render_template('ent_articles.html', articles=articles, title="Entertainment Articles")

@app.route('/science')
def science():
    articles = scienceArticles()
    return render_template('science_articles.html', articles=articles, title="Science Articles")

@app.route('/sports')
def sports():
    articles = sportArticles()
    return render_template('sport_articles.html', articles=articles, title="Sports Articles")

@app.route('/health')
def health():
    articles = healthArticles()
    return render_template('health_articles.html', articles=articles, title="Health Articles")

if __name__ == '__main__':
    app.run(debug=True)