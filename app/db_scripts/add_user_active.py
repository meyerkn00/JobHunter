from __future__ import annotations
import apsw
import apsw.ext
import apsw.bestpractice

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")
cursor = connection.cursor()


query = (
    """
        ALTER TABLE Users
            ADD COLUMN 'active' BOOLEAN NOT NULL CHECK (active IN (0,1)) DEFAULT 1;
        UPDATE Users
            SET active = 1;
    """
)
cursor.execute(query)