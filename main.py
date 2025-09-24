from scrapper import get_top_movies_by_genres
import random

def recommend_movie(genre_combo, scraped_movies):

    if scraped_movies:
        title, url = random.choice(scraped_movies)
        return f"Recommended from IMDb: {title} -> {url}"
    else:
        return f"No recommendation available for {', '.join(genre_combo)}."

if __name__ == "__main__":
    print("Welcome to Netflix Movie Recommendation Assistant 🎥")

    # Ask user for genres
    genres_input = input("Enter your favorite genres (comma separated, e.g., Action, Comedy): ")
    genres = [g.strip() for g in genres_input.split(",") if g.strip()]

    # Ask how many top movies per genre combo
    top = int(input("How many top movies from IMDb do you want to see for this genre combo?: "))

    movies = get_top_movies_by_genres(genres, top)

    if not movies:
        print(f"\nNo results found for genres: {', '.join(genres)}")
    else:
        print(f"\nTop {top} {', '.join(g.title() for g in genres)} Movies on IMDb:")
        for i, (title, url) in enumerate(movies, 1):
            print(f"{title} -> {url}")


        print("\n" + recommend_movie(genres, movies))
