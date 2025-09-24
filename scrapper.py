import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def get_top_movies_by_genres(genres, limit=10):

    genre_str = ",".join(g.strip().lower() for g in genres if g.strip())

    if not genre_str:
        return []

    url = (
        f"https://www.imdb.com/search/title/?genres={genre_str}"
        f"&explore=genres&title_type=feature&num_votes=25000,&sort=user_rating,desc"
    )

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    movies = soup.select("ul.ipc-metadata-list li")
    top_movies = []

    for movie in movies[:limit]:
        title_tag = movie.select_one("h3")
        link_tag = movie.select_one("a[href]")
        if not title_tag or not link_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = link_tag["href"]
        movieUrl = f"https://www.imdb.com{link}"

        top_movies.append((title, movieUrl))

    return top_movies
