import logging
import feedparser
from bs4 import BeautifulSoup
import os

logger = logging.getLogger(__name__)

RSS_URL = os.getenv("RSS_URL", "https://www.space.com/feeds/all")
last_articles = []

def check_rss():
    logger.info("Checking RSS feed")
    try:
        flux = feedparser.parse(RSS_URL)

        if flux.bozo:
            logger.info("Erreur lors de la récupération du flux RSS :", flux.bozo_exception)
            return
        
        for entree in reversed(flux.entries[10::-1]):
            identifiant = entree.id

            if identifiant not in last_articles:
                titre = entree.title
                lien = entree.link
                resume = entree.summary
                html_content = entree.dc_content
                soup = BeautifulSoup(html_content, 'html.parser')

                text = soup.get_text()

                last_articles.append(identifiant)
                if len(last_articles) > 10:
                    last_articles.pop(0)

    except Exception as e:
        print("Une erreur s'est produite :", str(e))
    