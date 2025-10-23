# api_handlers.py
import requests
from urllib.parse import urlencode
from config import Config


def normalize_city(city: str | None) -> str | None:
    """Capitalize each word in the city name for consistency."""
    if not city:
        return None
    return " ".join([w.capitalize() for w in city.split()])


class APIHandler:
    def __init__(self, ticketmaster_key: str = None):
        self.ticketmaster_key = ticketmaster_key or Config.TICKETMASTER_API_KEY

    # ---------- TICKETMASTER ----------
    def ticketmaster_search(self, keyword: str, city: str | None = None):
        if not self.ticketmaster_key:
            return [{
                "title": "Ticketmaster API key missing",
                "url": "",
                "start": ""
            }]

        city = normalize_city(city)
        base = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "apikey": self.ticketmaster_key,
            "keyword": keyword,
            "size": 8
        }
        if city:
            params["city"] = city

        try:
            r = requests.get(base, params=params, timeout=20)
            r.raise_for_status()
        except Exception as e:
            return [{
                "title": "Ticketmaster request failed",
                "url": "",
                "start": str(e)
            }]

        data = r.json()
        events = data.get("_embedded", {}).get("events", [])
        if not events:
            return []

        out = []
        for e in events:
            title = e.get("name", "Untitled event")
            url = e.get("url", "")
            start = e.get("dates", {}).get("start", {}).get("localDate", "")
            out.append({"title": title, "url": url, "start": start})
        return out