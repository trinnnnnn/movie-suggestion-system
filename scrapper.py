import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def clean_title(raw_title):
    #remove numbers from title
    return re.sub(r"^\d+\.\s*", "", raw_title).strip()

def get_top_movies_by_genres(genres, limit=10, sort="user_rating", order="desc"):
    genre_str = ",".join(g.strip().lower() for g in genres if g.strip())
    if not genre_str:
        return []

    #add num_votes filter only if not sorting by votes
    vote_filter = "&num_votes=25000," if sort != "num_votes" else ""

    url = (
        f"https://www.imdb.com/search/title/?genres={genre_str}"
        f"&explore=genres&title_type=feature{vote_filter}"
        f"&sort={sort},{order}"
    )

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    movies = soup.select("ul.ipc-metadata-list li.ipc-metadata-list-summary-item")
    if not movies:  # fallback in case IMDb changes layout again
        movies = soup.select("ul.ipc-metadata-list li")

    top_movies = []
    for movie in movies[:limit]:
        title_tag = movie.select_one("h3")
        link_tag = movie.select_one("a[href]")
        rating_tag = movie.select_one("span.ipc-rating-star--rating")

        if not title_tag or not link_tag:
            continue

        raw_title = title_tag.get_text(strip=True)
        title = clean_title(raw_title)  #remove numbering
        link = link_tag["href"]
        movieUrl = f"https://www.imdb.com{link}"
        rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        top_movies.append((title, movieUrl, rating))

    return top_movies
