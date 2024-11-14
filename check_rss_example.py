import json
import feedparser


RSS_URL: str = "https://www.space.com/feeds/all"
last_articles: json = {}

flux = feedparser.parse(RSS_URL)
print(len(flux.entries))

for entree in reversed(flux.entries[:10]):
    identifiant: str = entree.id

    if identifiant not in last_articles:
        titre: str = entree.title
        lien: str = entree.link
        resume: str = entree.summary
        print(entree.published)


        last_articles[identifiant] = {
            "title": titre,
            "link": lien,
            "summary": resume,
            "date": entree.published
        }
        while len(last_articles) > 10:
            oldest_key = next(iter(last_articles))
            del last_articles[oldest_key]

print("test")
for item in last_articles:
    print(last_articles[item]["date"])
