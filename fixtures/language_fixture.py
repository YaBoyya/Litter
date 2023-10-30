#!C://Coding/GitHub/Litter/.venv/scripts/activate
from pygments.lexers import get_all_lexers
import json


def to_json(model, languages):
    listed_data = []
    for i, language in enumerate(languages, 1):
        listed_data.append(
            {
                "model": model,
                "pk": i,
                "fields": {
                    "name": language
                }
            }
        )
    with open("./fixtures/language.json", "w") as outfile:
        json.dump(listed_data, outfile)


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([item[0]for item in LEXERS])
languages = sorted(LANGUAGE_CHOICES, key=str.casefold)
to_json("core.language", languages)
