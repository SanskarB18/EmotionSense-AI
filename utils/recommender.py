import json


with open("data/songs.json", "r") as f:
    songs_data = json.load(f)

with open("data/movies.json", "r") as f:
    movies_data = json.load(f)

with open("data/quotes.json", "r") as f:
    quotes_data = json.load(f)

with open("data/actions.json", "r") as f:
    actions_data = json.load(f)

with open("data/productivity.json", "r") as f:
    productivity_data = json.load(f)


def get_recommendations(emotion):

    emotion = emotion.lower()

    songs = songs_data.get(
        emotion,
        songs_data["neutral"]
    )

    movies = movies_data.get(
        emotion,
        movies_data["neutral"]
    )

    quote = quotes_data.get(
        emotion,
        "Stay positive and keep moving forward."
    )

    actions = actions_data.get(
        emotion,
        actions_data["neutral"]
    )

    productivity = productivity_data.get(
        emotion,
        productivity_data["neutral"]
    )

    return (
        songs,
        movies,
        quote,
        actions,
        productivity
    )