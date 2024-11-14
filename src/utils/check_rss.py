"""
Module to check RSS feed
"""
import logging
import os
import json
import feedparser
from bs4 import BeautifulSoup
from models import Article

logger = logging.getLogger(__name__)

RSS_URL: str = os.getenv("RSS_URL", "https://www.space.com/feeds/all")
last_articles: json = {}

def check_rss():
    """
    Check RSS feed
    """
    logger.info("Checking RSS feed")
    try:
        flux = feedparser.parse(RSS_URL)

        if flux.bozo:
            logger.info("Erreur lors de la récupération du flux RSS : %s", flux.bozo_exception)
            return

        for entree in reversed(flux.entries[:10]):
            identifiant: str = entree.id

            if identifiant not in last_articles:
                titre: str = entree.title
                lien: str = entree.link
                resume: str = entree.summary
                print(entree.published)
                html_content = entree.dc_content
                soup = BeautifulSoup(html_content, 'html.parser')

                text: str = soup.get_text()

                last_articles[identifiant] = Article(
                    title=titre,
                    link=lien,
                    summary=resume,
                    text=text
                )
                logger.info("Nouvel article : %s", titre)

                while len(last_articles) > 10:
                    oldest_key = next(iter(last_articles))
                    del last_articles[oldest_key]

    except (AttributeError, KeyError) as e:
        logger.error("Une erreur s'est produite : %s", str(e))
