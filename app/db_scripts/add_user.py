from __future__ import annotations
import apsw
import apsw.ext
import apsw.bestpractice
import itertools

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")
cursor = connection.cursor()

user_email = "craig+jh@themeyers.org"
user_keywords = ['Data', 'Research', 'Analyst']
user_companies = [1, 2, 3]

def create_user_id(user_email):
    user_id = connection.execute(
        "INSERT INTO Users ('email')"
        f"    VALUES ('{user_email}')"
        "     RETURNING Users.id"
    ).get
    return user_id

def add_user_companies(user_id, user_companies):
    data = [[*t] for t in zip(itertools.repeat(user_id), user_companies)]
    query = (
        "INSERT INTO User_Companies ('user_id', 'company_id')"
        f"     VALUES (?, ?)"
    )
    cursor.executemany(query, data)

def add_keywords(user_id, user_keywords):
    data = [[*t] for t in zip(itertools.repeat(user_id), user_keywords)]
    query = (
        "INSERT INTO Job_User_Keywords ('user_id', 'keyword')"
        f"     VALUES (?, ?)"
    )
    cursor.executemany(query, data)

def add_user(user_email, user_companies, user_keywords):
    user_id = create_user_id(user_email)
    add_user_companies(user_id, user_companies)
    add_keywords(user_id, user_keywords)
    print(f'Added user: ID = {user_id}')

add_user(user_email, user_companies, user_keywords)