import requests
import urllib.parse
import xml.etree.ElementTree as ET


def search_news(query, max_results=5):
    try:
        encoded_query = urllib.parse.quote(query)

        url = (
            "https://news.google.com/rss/search?"
            f"q={encoded_query}&hl=en-NG&gl=NG&ceid=NG:en"
        )

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        results = []

        for item in root.findall(".//item")[:max_results]:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            pub_date = item.findtext("pubDate", "")

            source = item.find("source")
            source_name = ""

            if source is not None:
                source_name = source.text or ""

            results.append({
                "title": title,
                "link": link,
                "source": source_name,
                "date": pub_date
            })

        return results

    except Exception as error:
        print("Online search error:", error)
        return []