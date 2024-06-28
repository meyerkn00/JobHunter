from __future__ import annotations
import apsw
import apsw.ext
import apsw.bestpractice

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")
cursor = connection.cursor()

# This file CLEARS the job database. Only run if you want to do that.

cursor.execute("""DELETE FROM "Job_Entries" WHERE ("rowid" > 0)""")