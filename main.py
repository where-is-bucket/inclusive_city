from textblob import TextBlob
from langdetect import detect
from deep_translator import GoogleTranslator


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


def calculate_inclusivity_score(reviews, wheelchairAccessibleParking=False, wheelchairAccessibleEntrance=False):
    relevant = []
    positive_mentions = 0
    total_mentions = len(reviews)

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
        return 0.0  # Немає згадок = 0 балів
    print(total_mentions, positive_mentions)
    ratio = positive_mentions / total_mentions  # частка позитивних згадок
    volume_bonus = min(1.0, total_mentions / 10)  # більше згадок = вищий бонус
    score = round(0.6 * ratio + 0.2 * volume_bonus + 0.15 * wheelchairAccessibleParking + 0.15 * wheelchairAccessibleEntrance, 2)  # ваги можна налаштовувати

    return score

dummy_reviews_1 = [
    "Дуже зручний вхід для візочників, є пандус!",
    "Люблю тутешні вказівники.",
    "Безбар’єрний доступ до туалету це класно!"
]

dummy_reviews_2 = [
    "Обожнюю тутешній ліфт і пандус",
    "Обожнюю тутешній ліфт і пандус",
    "Ненавиджу тутешній ліфт і пандус"
]

dummy_reviews_3 = [
    "Ненавиджу тутешні поручні",
    "Нічого не зроблено для людей зі слабким зором",
    "Дуже зручний вхід для візочників, є пандус!"
]

score = calculate_inclusivity_score(dummy_reviews_1, False, False)
print("Коефіцієнт потужності 1:", score)

score = calculate_inclusivity_score(dummy_reviews_2, False, False)
print("Коефіцієнт потужності 2:", score)

score = calculate_inclusivity_score(dummy_reviews_3, False, False)
print("Коефіцієнт потужності 3:", score)
