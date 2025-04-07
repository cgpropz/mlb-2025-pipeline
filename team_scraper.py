# team_scraper.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.baseball-reference.com"
LEAGUE_URL = f"{BASE_URL}/leagues/majors/2025.shtml"

def get_team_urls():
    response = requests.get(LEAGUE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    team_links = []
    table = soup.select_one("div#div_teams_standard_batting")
    
    for a in table.select("a"):
        href = a.get("href")
        if href and "/teams/" in href and href.endswith("/2025.shtml"):
            full_url = f"{BASE_URL}{href}"
            team_links.append(full_url)

    return team_links

if __name__ == "__main__":
    urls = get_team_urls()
    print(f"\nTotal teams found: {len(urls)}")
    for u in urls:
        print(u)
