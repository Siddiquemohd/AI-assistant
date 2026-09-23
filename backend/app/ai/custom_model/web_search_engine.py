import json
import re
import urllib.request
import urllib.parse

class WebSearchEngine:
    """
    Autonomous Web & Wikipedia Knowledge Search Engine.
    Queries Wikipedia API and web sources without requiring third-party API keys.
    """

    def search_wikipedia(self, query: str) -> dict:
        query_clean = query.strip()
        encoded_query = urllib.parse.quote(query_clean)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"

        headers = {"User-Agent": "ISAI-AutonomousAI/1.0 (personal AI assistant)"}

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    title = data.get("title", query_clean)
                    extract = data.get("extract", "No extract found.")
                    page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")

                    return {
                        "status": "Success",
                        "title": title,
                        "summary": extract,
                        "url": page_url
                    }
        except Exception as e:
            return {
                "status": "Error",
                "query": query_clean,
                "error": str(e),
                "summary": f"Could not fetch online summary for '{query_clean}'. Operating on local knowledge base."
            }

        return {
            "status": "NotFound",
            "summary": f"No online encyclopedia match found for '{query_clean}'."
        }
