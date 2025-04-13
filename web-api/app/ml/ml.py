from textblob import TextBlob
from langdetect import detect
from deep_translator import GoogleTranslator

from app.domain.place import Place

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

@staticmethod
def calculate_inclusivity_score(place: Place):
    reviews = [review.review_text for review in place.reviews]

    average = sum([review.review_score for review in place.reviews]) / len(place.reviews) if place.reviews else 0.0
    relevant = []
    positive_mentions = 0
    total_mentions = len(reviews)
    print(average)

    for review in reviews:
        text = review

        if not text.strip():
            continue

        try:
            lang = detect(text)
        except:
            continue

        if lang != "uk":
            continue

        text_lower = text.lower()
        if any(k in text_lower for k in ACCESSIBILITY_KEYWORDS):
            try:
                translated = translate_uk_to_en(text)
                sentiment = sentiments(str(translated))
                if sentiment > 0:
                    positive_mentions += 1
                relevant.append({
                    "original": text,
                    "translated": str(translated),
                    "sentiment": round(sentiment, 2)
                })
            except:
                continue

    if total_mentions == 0:
        return 0.0
    print(total_mentions, positive_mentions)
    ratio = positive_mentions / total_mentions
    score = round(0.7 * ratio + 0.3 * ((average - 1) / 4), 2)

    return score
