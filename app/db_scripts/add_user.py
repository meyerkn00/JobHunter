from __future__ import annotations
import apsw
import apsw.ext
import apsw.bestpractice

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")
cursor = connection.cursor()

user_email = "craig+jh@themeyers.org"
user_keywords = ['Data', 'Research', 'Analyst']
user_companies = [1, 2, 3]

user_id = cursor.execute(
    "INSERT INTO Users ('email')"
    f"    VALUES ({user_email})"
    "     RETURNING Users.id"
)

# WIP, need to batch insert and pull user id first
uc_query = (
    "INSERT INTO User_Companies ('user_id', 'company_id')"
    f"     VALUES (?, ?)"
)
cursor.executemany(uc_query, )

# WIP, need to batch insert
key_query = (
    "INSERT INTO User_Keywords ('user_id', 'keyword')"
    f"     VALUES (?, ?)"
)
