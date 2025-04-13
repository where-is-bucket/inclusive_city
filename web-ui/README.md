# Inclusive City ♿

**Inclusive City** — це вебзастосунок, який допомагає знаходити місця для людей з обмеженими можливостями у місті: локації з пандусами, адаптованими туалетами, тактильними елементами тощо.

## Особливості

- Пошук закладів, які мають ознаки доступності
- Інтеграція з Google Maps API
- Підтримка фільтрів за типом адаптації
- Інтуїтивний інтерфейс користувача
- REST API на FastAPI
- Дані з lun.ua + додаткове збагачення через Google Places API

## Технології

- **Frontend**: React (Vite), JavaScript, HTML, CSS
- **Backend**: Python, FastAPI
- **Docker + Docker Compose**
- **API**: Google Maps Places API, lun.ua API
- **Machine Learning**: Tone Recognition, Lang Detect, Оцінка безбар'єрності

## Швидкий старт

### Вимоги

- Встановлений [Docker](https://docs.docker.com/get-docker/)
- Встановлений [Docker Compose](https://docs.docker.com/compose/)

### ⚙️ Налаштування

1. Створіть `.env` файл у корені репозиторію (біля `docker-compose.yml`) з вашим Google API ключем:

```env
MONGO_HOSTNAME=
MONGO_INITDB_ROOT_USERNAME=YOUR_USERNAME
MONGO_INITDB_ROOT_PASSWORD=YOUR_PASSWORD

GOOGLE_API_TOKEN=YOUR_GOOGLE_API_TOKEN

MONGO_CONNECTION=mongodb://MONGO_INITDB_ROOT_USERNAME:MONGO_INITDB_ROOT_PASSWORD@MONGO_HOSTNAME:27017

GOOGLE_MAP_ID=

WEB_API_BASE_URL=
ROUTE_MANAGEMENT_API_BASE_URL=
```

2. Запустіть сервіс:

```bash
docker compose up --build
```

### Зупинка

```bash
docker compose down
```

## Структура проєкту

```bash
inclusive_city/
├── backend/              # FastAPI сервер
├── frontend/             # React застосунок (Vite)
├── docker-compose.yml    # Конфігурація для запуску
└── .env                  # Ключі та змінні середовища
```

## Секрети та ключі

Проєкт використовує ключі Google Maps API (зокрема **Places API**, **Directions API** та **Maps JavaScript API**).

### Як отримати API-ключ:

1. Перейдіть у [Google Cloud Console](https://console.cloud.google.com/).
2. Створіть новий проєкт або виберіть вже існуючий.
3. Перейдіть у **APIs & Services → Credentials**.
4. Натисніть **"Create credentials" → API key**.
5. Скопіюйте ключ і додайте у `.env` файл у корені проєкту:

## Зв'язок

Проєкт розроблений з метою покращення доступності міського середовища для людей з інвалідністю.

Контакт: [@endeavour93](https://t.me/endeavour93) в телеграмі

---
    Разом зробимо міста більш інклюзивними 💪