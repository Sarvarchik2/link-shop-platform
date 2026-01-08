
import json
import os

files = [
    "frontend/locales/uz.json",
    "frontend/locales/ru.json",
    "frontend/locales/en.json",
    "frontend/i18n/locales/uz.json",
    "frontend/i18n/locales/ru.json",
    "frontend/i18n/locales/en.json"
]

for f in files:
    if os.path.exists(f):
        try:
            with open(f, 'r', encoding='utf-8') as file:
                json.load(file)
            print(f"{f}: VALID")
        except json.JSONDecodeError as e:
            print(f"{f}: INVALID - {e}")
    else:
        print(f"{f}: NOT FOUND")
