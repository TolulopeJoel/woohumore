import requests
from bs4 import BeautifulSoup

def scrape_news(url, link__tag, link__class, title__tag, title__class):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    link = soup.find(link__tag, class_=link__class)
    title = link.find(title__tag) if link else None
    article_title = title.text.strip()

    if (article_link := link.get('href')) is None:
        article_link = title.get('href')

    print(f"Title: {article_title}")
    print(f"Link: {article_link}")

def lad_bible():
    scrape_news("https://www.ladbible.com/weird", "a", "title css-vqy1ed", 'h3', '')

def the_week():
    scrape_news("https://theweek.com/tag/odd-news", "a", "listing__link", 'h2', '')

def todaynews():
    scrape_news("https://www.today.com/news/good-news", "a", "", 'h3', '')

def goodnewstwork():
    scrape_news("https://www.goodnewsnetwork.org/", "h3", "entry-title td-module-title", 'a', '')

# Call the functions to test
lad_bible()
the_week()
goodnewstwork()
# todaynews()
