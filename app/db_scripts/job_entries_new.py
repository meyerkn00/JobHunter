from __future__ import annotations
import apsw
import apsw.ext
import apsw.bestpractice

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")
cursor = connection.cursor()

# Code ran to rebuilt Job_Entries database to fix unique key and foreign key issues. Also removed user.id

# cursor.execute("DROP TABLE Job_Entries")
# cursor.execute("""
#                CREATE TABLE 'Job_Entries' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
# 							'title' TEXT, 
# 							'url' TEXT , 
# 							'company_id' INTEGER, 
# 							'last_update' DATETIME DEFAULT CURRENT_TIMESTAMP, 
# 							UNIQUE (`title`, `url`, `company_id`), 
# 							FOREIGN KEY (company_id) REFERENCES Companies (id) )
#                """)