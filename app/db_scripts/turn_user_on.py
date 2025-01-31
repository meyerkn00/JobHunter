from __future__ import annotations
import apsw
import apsw.ext
import apsw.bestpractice

"""
    Edit the variable below with the User_id of the user you would like to turn on
"""

USER_ID = [1]

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")
cursor = connection.cursor()

query = (
    """
        UPDATE Users
            SET active = 1
            WHERE id = ?;
    """
)
cursor.execute(query, USER_ID)
print(f'Activated User {USER_ID}')