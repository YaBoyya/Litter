#!C://Coding/GitHub/Litter/.venv/scripts/activate
from datetime import datetime, timedelta
import json
from os import walk
import random


from django.contrib.auth.hashers import PBKDF2PasswordHasher
import faker
from pygments.lexers import get_all_lexers


hasher = PBKDF2PasswordHasher()
faker = faker.Faker()
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([item[0]for item in LEXERS])
languages = sorted(LANGUAGE_CHOICES, key=str.casefold)
language_count = len(languages)
user_count = 3000
post_count = 5 * user_count
comment_count = 10 * post_count
postvote_count = 10 * comment_count
commentvote_count = 10 * postvote_count


def get_files_paths(path: str):
    loc = next(walk(path), ([], None, []))
    dirname = loc[0][8:] + '/'
    filenames = loc[2]
    return [dirname + filename for filename in filenames]


def generate_time(end_time=None):
    start = datetime.now()
    end = end_time or (datetime.now() - timedelta(days=365))
    return start + (end - start) * random.random()


def not_naive(time):
    return str(time).replace(" ", "T")[:-3] + "Z"


def pseudorandom(M, N, max):
    tups = []
    i = 1
    while (True):
        if i % 1000 == 0:
            print(i)
        tup = (random.randrange(1, M), random.randrange(1, N))
        tups.append(tup)
        if i % 1500000 == 0:
            tups = list(set(tups))
            i = len(tups)
            if i == max:
                break
        i += 1
    return tups


def language_fixture():
    listed_data = []
    for i, language in enumerate(languages, 1):
        listed_data.append(
            {
                "model": "core.language",
                "pk": i,
                "fields": {
                    "name": language
                }
            }
        )
    with open("./fixtures/language.json", "w") as outfile:
        json.dump(listed_data, outfile)


def litteruser_fixture():
    listed_data = []
    profile_pics = get_files_paths("./media/fixture_profile_pics")
    profile_pics.append("default_pp.png")
    for i in range(1, user_count):
        join = generate_time()
        username = faker.unique.user_name()
        if i % 100 == 0:
            print(f"{i}/{user_count}")
        listed_data.append(
            {
                "model": "users.litteruser",
                "pk": i,
                "fields": {
                    "password": hasher.encode(faker.password(), str(i)),
                    "last_login": not_naive(generate_time(end_time=join)),
                    "is_superuser": False,
                    "first_name": "",
                    "last_name": "",
                    "is_staff": False,
                    "is_active": True,
                    "date_joined": not_naive(join),
                    "email": faker.email(),
                    "username": username,
                    "usertag": username.lower(),
                    "bio": None,
                    "picture": random.choice(profile_pics),
                    "groups": [],
                    "user_permissions": [],
                    "following": sorted(
                        [random.randrange(1, user_count)
                         for r in range(random.randrange(1, 200))]
                        ),
                    "languages": sorted(
                        [random.randrange(1, language_count)
                         for r in range(random.randrange(1, 20))]
                        )
                }
            }
        )
    with open("./fixtures/litteruser.json", "w") as outfile:
        json.dump(listed_data, outfile)


def post_fixture():
    listed_data = []
    post_pics = get_files_paths("./media/fixture_post_pics")
    for i in range(1, post_count):
        if i % 1000 == 0:
            print(f"{i}/{post_count}")
        listed_data.append(
            {
                "model": "core.post",
                "pk": i,
                "fields":
                {
                    "user": random.randrange(1, user_count),
                    "title": faker.catch_phrase(),
                    "text": faker.paragraph(nb_sentences=3,
                                            variable_nb_sentences=True),
                    "picture": random.choice(post_pics)
                    if random.random() > 0.4 else "",
                    "difficulty": random.choice(["E", "M", "H"]),
                    "views": random.randrange(post_count),
                    "created": not_naive(generate_time()),
                    "was_edited": random.choice([False, True]),
                    "languages": sorted(
                        [random.randrange(1, language_count)
                         for r in range(random.randrange(1, 5))]
                        )
                }
            }
        )
    with open("./fixtures/post.json", "w") as outfile:
        json.dump(listed_data, outfile)


def comment_fixture():
    listed_data = []
    for i in range(1, comment_count):
        if i % 1000 == 0:
            print(f"{i}/{comment_count}")
        listed_data.append(
            {
                "model": "core.comment",
                "pk": i,
                "fields":
                {
                    "user": random.randrange(1, user_count),
                    "post": random.randrange(1, post_count),
                    "text": faker.sentence(),
                    "created": not_naive(generate_time()),
                    "was_edited": random.choice([False, True])
                }
            }
        )
    with open("./fixtures/comment.json", "w") as outfile:
        json.dump(listed_data, outfile)


def postvote_fixture():
    listed_data = []
    rand_id = pseudorandom(user_count, post_count, postvote_count)
    print("Git")
    for i in range(1, postvote_count):
        user_id, post_id = rand_id[i-1]
        if i % 1000 == 0:
            print(f"{i}/{postvote_count}")
        listed_data.append(
            {
                "model": "core.postvote",
                "pk": i,
                "fields":
                {
                    "user": user_id,
                    "post": post_id,
                    "created": not_naive(generate_time())
                }
            }
        )
    with open("./fixtures/postvote.json", "w") as outfile:
        json.dump(listed_data, outfile)


def commentvote_fixture():
    listed_data = []
    rand_id = pseudorandom(user_count, comment_count, commentvote_count)
    print("Git")
    for i in range(1, commentvote_count):
        user_id, comment_id = rand_id[i-1]
        if i % 1000 == 0:
            print(f"{i}/{commentvote_count}")
        listed_data.append(
            {
                "model": "core.commentvote",
                "pk": i,
                "fields":
                {
                    "user": user_id,
                    "comment": comment_id,
                    "created": not_naive(generate_time())
                }
            }
        )
    with open("./fixtures/commentvote.json", "w") as outfile:
        json.dump(listed_data, outfile)


# language_fixture()
# print("Language done.")
litteruser_fixture()
print("LitterUser done.")
post_fixture()
print("Post done.")
# comment_fixture()
# print("Comment done.")
# postvote_fixture()
# print("PostVote done.")
# commentvote_fixture()
# print("CommentVote done.")
