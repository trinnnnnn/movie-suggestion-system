import random, os, time, sys, subprocess, importlib
def install_and_import(package, module_name=None):
    try:
        if module_name is None:
            module_name = package
        importlib.import_module(module_name)
    except ImportError:
        print(f"⚠️ {package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully.")

#required modules
requirements = [
    ("requests", "requests"),
    ("beautifulsoup4", "bs4")
]

for pkg, mod in requirements:
    install_and_import(pkg, mod)

from scrapper import get_top_movies_by_genres


# genre list
GENRES = [
    "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
    "Documentary", "Drama", "Family", "Fantasy", "Film-Noir", "Game-Show", "History", "Horror",
    "Music", "Musical", "Mystery", "News", "Reality-TV", "Romance", "Sci-Fi", "Sport", "Talk-Show", "Thriller", "War",
    "Western"
]

def recommend_movies(scraped_movies, count=3):
    if scraped_movies:
        picks = random.sample(scraped_movies, k=min(count, len(scraped_movies)))
        return picks
    else:
        return []

def show_genre_list():
    print("\nAvailable Genres:")
    for i, g in enumerate(GENRES, 1):
        print(f"{i}. {g}")
    print(f"{len(GENRES)+1}. Surprise Me 🎲")

def save_to_file(movies, genres):
    # save file into history folder
    os.makedirs("history", exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"history/{'_'.join(genres)}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Top {len(movies)} {', '.join(genres)} Movies from IMDb:\n")
        for title, url, rating in movies:
            f.write(f"{title} ⭐ {rating} -> {url}\n")

    print(f"\n💾 Results saved to {filename}")

def save_watchlist(movie, filename="watchlist.txt"):
    entry = f"{movie[0]} ⭐ {movie[2]} -> {movie[1]}"

    # check for duplicates
    existing_movies = set()
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            existing_movies = {line.strip() for line in f if line.strip()}

    if entry in existing_movies:
        print(f"⚠️ Skipped duplicate: {movie[0]}")
    else:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        print(f"💾 Added to Watchlist: {movie[0]}")

def browse_movies():
    show_genre_list()
    choices = input("\nEnter genre numbers (comma separated, e.g., 1,5,7 or Surprise Me): ")
    selected = []
    for c in choices.split(","):
        c = c.strip()
        if c.isdigit():
            num = int(c)
            if 1 <= num <= len(GENRES):
                selected.append(GENRES[num-1])
            elif num == len(GENRES)+1:
                selected = [random.choice(GENRES)]
                print(f"🎲 Surprise! We'll show you movies from {selected[0]}")
                break

    if not selected:
        print("⚠️ Invalid selection. Returning to main menu...")
        return

    try:
        top = int(input(f"How many top movies do you want to see (Limit 25) for {', '.join(selected)}?: "))
        if top > 25:
            print("⚠️ Defaulting to 25 as it's the limit")
            top = 25
        if top <= 0:
            raise ValueError
    except ValueError:
        print("⚠️ Invalid number. Returning to main menu...")
        return

    # sorting options
    sort_options = {
        "1": "user_rating",
        "2": "year",
        "3": "num_votes",
        "4": "alpha",
        "5": "boxoffice_gross_us",
        "6": "runtime",
        "7": "release_date",
        "8": "popularity"
    }

    print("\nSort by:")
    print("1. Rating")
    print("2. Year")
    print("3. Number of Votes")
    print("4. Alphabetical (Title)")
    print("5. Box Office (US Gross)")
    print("6. Runtime")
    print("7. Release Date")
    print("8. Popularity")

    sort_choice = input("Choose sort option (default: 1): ")
    sort = sort_options.get(sort_choice, "user_rating")
    if sort_choice not in sort_options:
        print("⚠️ Invalid choice. Defaulting to Rating.")
        sort = "user_rating"

    order_choice = input("Ascending (a) or Descending (d)? (default: d): ").lower()
    order = "asc" if order_choice == "a" else "desc"
    if order_choice not in ["a", "d", ""]:
        print("⚠️ Invalid choice. Defaulting to Descending.")
        order = "desc"

    # fetch movies
    movies = get_top_movies_by_genres(selected, top, sort=sort, order=order)

    if not movies:
        print(f"\n⚠️ No results for genres: {', '.join(selected)}")
        return

    print(f"\n📌 Top {top} {', '.join(selected)} Movies (sorted by {sort}, {order}):")
    for i, (title, url, rating) in enumerate(movies, 1):
        print(f"{i}. {title} ⭐ {rating} -> {url}")

    # random recommendations
    picks = recommend_movies(movies, count=3)
    if picks:
        print("\n🎯 Recommended Picks for You:")
        for idx, (title, url, rating) in enumerate(picks, 1):
            print(f"{idx}. {title} ⭐ {rating} -> {url}")

    # add any movie from the list
    while True:
        add_choice = input("\nDo you want to add a movie from the above list to your Watchlist? (y/n): ").lower()
        if add_choice != "y":
            break
        try:
            pick_num = int(input(f"Enter the number of the movie to add (1-{len(movies)}): "))
            if 1 <= pick_num <= len(movies):
                save_watchlist(movies[pick_num-1])
            else:
                print("⚠️ Invalid selection.")
        except ValueError:
            print("⚠️ Invalid input.")

    save_to_file(movies, selected)

def view_watchlist(filename="watchlist.txt"):
    if not os.path.exists(filename):
        print("\n📂 Your Watchlist is empty.")
        input("\nPress Enter to return to main menu...")
        return

    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("\n📂 Your Watchlist is empty.")
    else:
        print("\n📂 Your Watchlist:")
        for i, entry in enumerate(lines, 1):
            print(f"{i}. {entry}")

    input("\nPress Enter to return to main menu...")

if __name__ == "__main__":
    print("=== Movie Recommendation Assistant 🎥 ===")

    while True:
        print("\n===== Main Menu =====")
        print("1. Browse Movies by Genre")
        print("2. View Watchlist")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            browse_movies()
        elif choice == "2":
            view_watchlist()
        elif choice == "3":
            print("👋 Thanks for using the Movie Assistant. Goodbye!")
            break
        else:
            print("⚠️ Invalid option. Please choose again.")
