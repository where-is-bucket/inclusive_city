# import dataclasses
# from typing import List

import math
# from pydantic_core.core_schema import plain_serializer_function_ser_schema
from textblob import TextBlob
from langdetect import detect
from deep_translator import GoogleTranslator
# from pydantic import BaseModel
#
# @dataclasses.dataclass
# class Review:
#     review_text: str
#     review_score: int
#
#
# class Place(BaseModel):
#     reviews: List[Review] = []

ACCESSIBILITY_KEYWORDS = [
    "пандус", "безбар’єрн", "доступ",
    "бар’єр", "перешкода","перепон",
    "широкий прохід", "широкі двері", "автоматичні двері", "вхід з вулиці",
    "інвалід", "візок", "візочники",
    "місце для інвалідів", "туалет для інвалідів", "паркомісце для інвалідів",
    "ліфт", "підйомник", "платформа",
    "доступний туалет", "туалет для інвалідів", "санвузол", "громадський туалет", "унітаз з поручнями",
    "інвалідне паркомісце", "паркінг для інвалідів", "доступна парковка", "широке паркомісце",
    "навігація для незрячих", "шрифт Брайля", "озвучка", "вказівники", "дублювання жестовою мовою",
    "сурдопереклад", "аудіогід", "слабозорий", "поганий зір", "поручні", "контрастна розмітка"
]

def translate_uk_to_en(text):
    return GoogleTranslator(source='uk', target='en').translate(text)


def sentiments(text):
    text = TextBlob(text)
    return text.sentiment.polarity


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def calculate_inclusivity_score(place: Place):
    reviews = [review.review_text for review in place.reviews]
    scores = [review.review_score for review in place.reviews if review.review_score is not None]

    if not scores:
        return 0.0

    average = sum(scores) / len(scores)
    relevant = []
    positive_mentions = 0
    relevant_mentions = 0

    for review in reviews:
        if not review.strip():
            continue

        try:
            lang = detect(review)
        except:
            continue

        if lang != "uk":
            continue

        text_lower = review.lower()
        if any(k in text_lower for k in ACCESSIBILITY_KEYWORDS):
            try:
                translated = translate_uk_to_en(review)
                sentiment = sentiments(str(translated))
                relevant_mentions += 1
                if sentiment > 0:
                    positive_mentions += 1
                relevant.append({
                    "original": review,
                    "translated": str(translated),
                    "sentiment": round(sentiment, 2)
                })
            except:
                continue

    if relevant_mentions == 0:
        sentiment_score = 0.0
    else:
        sentiment_score = positive_mentions / relevant_mentions

    normalized_rating = (average - 1) / 4  # (1 = 0, 5 = 1)

    raw_score = 0.6 * sentiment_score + 0.4 * normalized_rating

    scaled_score = sigmoid(raw_score * 5 - 2.5)  # центруємо біля 0.5

    return round(scaled_score, 2)


# review_1 = Review(review_score = 5, review_text = "Люблю пандус")
# review_2 = Review(review_score = 5, review_text = "Люблю ліфт")
# place = Place(reviews=[review_1, review_2])
#
# score = calculate_inclusivity_score(place)
# print(score)
