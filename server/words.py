import random

WORDS = [
    "apple",
    "window",
    "planet",
    "coffee",
    "river",
    "chair",
    "keyboard",
    "forest",
    "camera",
    "orange",
    "banana",
    "silver",
    "bridge",
    "monitor",
    "school",
    "guitar",
    "winter",
    "yellow",
    "garden",
    "engine"
]


def generate_words(count=20):
    return " ".join(random.sample(WORDS, count))