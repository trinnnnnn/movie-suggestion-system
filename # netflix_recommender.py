# netflix_recommender.py
# Simple Netflix-style movie recommendation assistant
# Part 2: Interactive Program (Assignment)

def recommend_movie(genre):
    if genre.lower() == "action":
        return "🎬 Recommended: John Wick (2014) - A retired hitman seeks vengeance."
    elif genre.lower() == "comedy":
        return "😂 Recommended: The Mask (1994) - A man discovers a magical mask."
    elif genre.lower() == "romance":
        return "❤️ Recommended: The Notebook (2004) - A timeless love story."
    elif genre.lower() == "sci-fi":
        return "🚀 Recommended: Inception (2010) - Dreams within dreams."
    elif genre.lower() == "horror":
        return "👻 Recommended: The Conjuring (2013) - Paranormal investigators face dark forces."
    else:
        return "❌ Sorry, genre not available. Try Action, Comedy, Romance, Sci-Fi, or Horror."

if __name__ == "__main__":
    print("Welcome to Netflix Movie Recommendation Assistant 🎥")
    genre = input("Enter your favorite genre (Action, Comedy, Romance, Sci-Fi, Horror): ")
    print(recommend_movie(genre))
