from quote import quote
import random


def generate_quote(words=("science", "music", "engineering")):
    choice = random.choice(words)
    res = quote(choice, limit=100)
    random_number = random.randint(1, 100)
    print(f"We want to remind you: {res[random_number]['quote']} ({res[random_number]['author']})")
