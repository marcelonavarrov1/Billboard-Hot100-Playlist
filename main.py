from bs4 import BeautifulSoup
import requests


response = requests.get("https://news.ycombinator.com/news")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

article_upvote = soup.find(name="span", class_= "score", id= "score_41389185").getText()
print(article_upvote)