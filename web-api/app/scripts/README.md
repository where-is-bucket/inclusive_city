1. Parse facilities:

From root: `python -m app.scripts.parse_facilities`

That will create the following content in `parsed_lun_facilities.json`:

```txt
Ширина тротуару перед будівлею не менше 1.8 м
Ширина тротуару у парку, сквері не менше 1.8 м
Шляхи евакуації промарковані візуально та тактильно й є доступними для маломобільних груп населення (люди з інвалідністю, вагітні, люди старшого віку тощо)
Шляхи евакуації промарковані візуально та тактильно та є доступними для маломобільних груп населення
Шрифт Брайля
```

2. See facilities

The `sample_facilities.json` file contains prepared content for seeding: 

```json
[
    {
      "text": "Засоби акустичної орієнтації  у закладі",
      "disability_types": [
        "VISUAL_IMPAIRMENT"
      ]
    },
    {
      "text": "Засоби акустичної орієнтації  у закладі (аудіосповіщення)",
      "disability_types": [
        "VISUAL_IMPAIRMENT"
      ]
    },
    {
      "text": "Засоби акустичної орієнтації (аудіосповіщення, шритф Брайля)",
      "disability_types": [
        "VISUAL_IMPAIRMENT",
        "HEARING_IMPAIRMENT"
      ]
    }
]
```

From root: `python -m app.scripts.seed_facilities`