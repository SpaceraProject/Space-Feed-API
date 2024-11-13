import logging
import feedparser
from bs4 import BeautifulSoup
import os
import json

logger = logging.getLogger(__name__)

RSS_URL: str = os.getenv("RSS_URL", "https://www.space.com/feeds/all")
last_articles: json = {}

def check_rss():
    logger.info("Checking RSS feed")
    try:
        flux = feedparser.parse(RSS_URL)

        if flux.bozo:
            logger.info("Erreur lors de la récupération du flux RSS :", flux.bozo_exception)
            return
        
        for entree in reversed(flux.entries[9::-1]):
            identifiant: str = entree.id
            
            if identifiant not in last_articles.keys():
                titre: str = entree.title
                lien: str = entree.link
                resume: str = entree.summary
                html_content = entree.dc_content
                soup = BeautifulSoup(html_content, 'html.parser')

                text: str = soup.get_text()

                last_articles[identifiant] = {
                    "titre": titre,
                    "lien": lien,
                    "resume": resume,
                    "texte": text
                }
                logger.info(f"Nouvel article : {titre}")
                if len(last_articles) > 10:
                    last_articles.popitem(last=False)

    except Exception as e:
        print("Une erreur s'est produite :", str(e))
    