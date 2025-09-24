import requests
from bs4 import BeautifulSoup

top = int(input("How many top movies do you want to see?: "))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

res = requests.get("https://www.imdb.com/chart/top/", headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

#movies element
movies = soup.select("ul.ipc-metadata-list li")

for movie in movies[:top]:  #top 10 movies
    title_tag = movie.select_one("h3")
    if not title_tag:
        continue
    
    title = title_tag.get_text(strip=True)
    link = movie.find("a", href=True)["href"]
    movieUrl = f"https://www.imdb.com{link}"
    
    print(title, "->", movieUrl)
