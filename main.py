from scrapper import get_top_movies_by_genres
import random

# List of genres available on IMDb
GENRES = [
    "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music",
    "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"
]

watchlist = []  # global watchlist

def recommend_movies(scraped_movies, count=3):
    """Pick multiple random movies from scraped list."""
    if scraped_movies:
        picks = random.sample(scraped_movies, k=min(count, len(scraped_movies)))
        return picks
    else:
        return []

def show_genre_list():
    """Display available genres with numbers."""
    print("\nAvailable Genres:")
    for i, g in enumerate(GENRES, 1):
        print(f"{i}. {g}")
    print(f"{len(GENRES)+1}. Surprise Me 🎲")

def save_to_file(filename, movies, genres):
    """Save movie recommendations to a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Top {len(movies)} {', '.join(genres)} Movies from IMDb:\n")
        for title, url, rating in movies:
            f.write(f"{title} ⭐ {rating} -> {url}\n")
    print(f"\n💾 Results saved to {filename}")

def save_watchlist(filename="watchlist.txt"):
    """Save watchlist to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Your Watchlist:\n")
        for title, url, rating in watchlist:
            f.write(f"{title} ⭐ {rating} -> {url}\n")
    print(f"💾 Watchlist saved to {filename}")

def browse_movies():
    """Browse movies by genre and manage recommendations."""
    show_genre_list()
    choices = input("\nEnter genre numbers (comma separated, e.g., 1,5,7 or pick Surprise Me): ")
    selected = []
    for c in choices.split(","):
        c = c.strip()
        if c.isdigit():
            num = int(c)
            if 1 <= num <= len(GENRES):
                selected.append(GENRES[num-1])
            elif num == len(GENRES)+1:  # Surprise Me option
                selected = [random.choice(GENRES)]
                print(f"🎲 Surprise! We'll show you movies from {selected[0]}")
                break

    if not selected:
        print("⚠️ Invalid selection. Returning to main menu...")
        return

    try:
        top = int(input(f"How many top movies do you want to see for {', '.join(selected)}?: "))
        if top <= 0:
            raise ValueError
    except ValueError:
        print("⚠️ Invalid number entered. Returning to main menu...")
        return

    # Scrape movies
    movies = get_top_movies_by_genres(selected, top)

    if not movies:
        print(f"\n⚠️ No results found for genres: {', '.join(selected)}")
        return
    else:
        print(f"\n📌 Top {top} {', '.join(selected)} Movies on IMDb:")
        for i, (title, url, rating) in enumerate(movies, 1):
            print(f"{i}. {title} ⭐ {rating} -> {url}")

        # Multiple random recommendations
        picks = recommend_movies(movies, count=3)
        if picks:
            print("\n🎯 Recommended Picks for You:")
            for idx, (title, url, rating) in enumerate(picks, 1):
                print(f" {idx}. {title} ⭐ {rating} -> {url}")

        # Ask if user wants to add to watchlist
        add_choice = input("\nDo you want to add a recommended movie to your Watchlist? (y/n): ").lower()
        if add_choice == "y":
            try:
                pick_num = int(input("Enter the number of the recommended movie to add: "))
                if 1 <= pick_num <= len(picks):
                    watchlist.append(picks[pick_num-1])
                    print(f"✅ Added to Watchlist: {picks[pick_num-1][0]}")
                    save_watchlist()
                else:
                    print("⚠️ Invalid selection. Nothing added.")
            except ValueError:
                print("⚠️ Invalid input. Nothing added.")

        # Save results of this browsing
        save_to_file("recommendations.txt", movies, selected)

def view_watchlist():
    """View current watchlist."""
    if not watchlist:
        print("\n📂 Your Watchlist is empty.")
    else:
        print("\n📂 Your Watchlist:")
        for i, (title, url, rating) in enumerate(watchlist, 1):
            print(f"{i}. {title} ⭐ {rating} -> {url}")
    input("\nPress Enter to return to main menu...")

if __name__ == "__main__":
    print("=== Netflix Movie Recommendation Assistant 🎥 ===")

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
            print("👋 Thanks for using the Netflix Movie Assistant. Goodbye!")
            break
        else:
            print("⚠️ Invalid option. Please choose again.")

