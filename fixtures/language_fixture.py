#!C://Coding/GitHub/Litter/.venv/scripts/activate
import json
from pygments.lexers import get_all_lexers
from uuid import uuid4


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([item[0]for item in LEXERS])
languages = sorted(LANGUAGE_CHOICES, key=str.casefold)

language_data = []
chatroom_data = []
for i, language in enumerate(languages, 1):
    chatroom_data.append(
        {
            "model": "chat.chatroom",
            "pk": i,
            "fields": {
                "uuid": str(uuid4()),
                "title": language,
                "is_private": False
            }
        }
    )
    language_data.append(
        {
            "model": "core.language",
            "pk": i,
            "fields": {
                "name": language
            }
        }
    )
with open("./fixtures/language.json", "w") as outfile:
    json.dump(language_data, outfile)

with open("./fixtures/chatroom.json", "w") as outfile:
    json.dump(chatroom_data, outfile)
