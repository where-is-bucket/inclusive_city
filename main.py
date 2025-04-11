from textblob import TextBlob
from langdetect import detect
from deep_translator import GoogleTranslator

ACCESSIBILITY_KEYWORDS = [
    "інвалід", "пандус", "доступ", "доступний", "ліфт",
    "бар’єр", "візок", "сходи", "безбар’єрний", "туалет", "перешкод"
]

def translate_uk_to_en(text):
    return GoogleTranslator(source='uk', target='en').translate(text)


def sentiments(text):
    text = TextBlob(text)
    return text.sentiment.polarity


def calculate_inclusivity_score(reviews):
    relevant = []
    positive_mentions = 0
    total_mentions = 0
    wheelchairAccessibleParking = 0
    wheelchairAccessibleEntrance = 0

    for review in reviews:
        text = review.get("text", "")

        if "wheelchairAccessibleParking" in review:
            wheelchairAccessibleParking = 1 if review["wheelchairAccessibleParking"] == "true" else 0

        if "wheelchairAccessibleEntrance" in review:
            wheelchairAccessibleEntrance = 1 if review["wheelchairAccessibleEntrance"] == "true" else 0

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
            total_mentions += 1
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
        return 0.0  # Немає згадок = 0 балів
    print(positive_mentions)
    ratio = positive_mentions / total_mentions  # частка позитивних згадок
    volume_bonus = min(1.0, total_mentions / 10)  # більше згадок = вищий бонус
    score = round(0.7 * ratio + 0.3 * volume_bonus + 0.2 * wheelchairAccessibleParking + 0.2 * wheelchairAccessibleEntrance, 2)  # ваги можна налаштовувати

    return score

dummy_reviews_1 = [
    {"text": "Дуже зручний вхід для візочників, є пандус!"},
    {"text": "Люблю сходи."},
    {"text": "Безбар’єрний доступ до туалету це класно!"},
    {"wheelchairAccessibleParking": "true"},
    {"wheelchairAccessibleEntrance": "true"}
]

dummy_reviews_2 = [
    {"text": "Обожнюю тутешній ліфт і пандус"},
    {"text": "Обожнюю тутешній ліфт і пандус"},
    {"text": "Обожнюю тутешній ліфт і пандус"},
    {"wheelchairAccessibleParking": "false"},
    {"wheelchairAccessibleEntrance": "false"}
]

dummy_reviews_3 = [
    {"text": "Ненавиджу тутешні сходи"},
    {"text": "Нічого не зроблено для людей зі слабким зором"},
    {"text": "Дуже зручний вхід для візочників, є пандус!"},
    {"wheelchairAccessibleParking": "false"},
    {"wheelchairAccessibleEntrance": "false"}
]

score = calculate_inclusivity_score(dummy_reviews_1)
print("Коефіцієнт потужності 1:", score)

score = calculate_inclusivity_score(dummy_reviews_2)
print("Коефіцієнт потужності 2:", score)

score = calculate_inclusivity_score(dummy_reviews_3)
print("Коефіцієнт потужності 3:", score)
