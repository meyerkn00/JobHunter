from __future__ import annotations
import apsw
import apsw.ext
import apsw.bestpractice

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")
cursor = connection.cursor()

# Uncomment and run the following if you need to build/rebuild the database. Make sure the resulting file ends up in the root folder.

# cursor.execute("""
# ----
# -- phpLiteAdmin database dump (https://www.phpliteadmin.org/)
# -- phpLiteAdmin version: 1.9.8.2
# -- Exported: 10:58am on July 9, 2024 (EDT)
# -- database file: ./job_listings.sqlite3
# ----
# BEGIN TRANSACTION;

# ----
# -- Table structure for Users
# ----
# CREATE TABLE 'Users' (
#     'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     'email' TEXT UNIQUE,
#     'last_update' DATETIME DEFAULT CURRENT_TIMESTAMP
#       );

# ----
# -- Data dump for Users, a total of 2 rows
# ----
# INSERT INTO "Users" ("id","email","last_update") VALUES ('1','karl+jh@themeyers.org','CURRENT_TIMES');
# INSERT INTO "Users" ("id","email","last_update") VALUES ('2','craig+jh@themeyers.org','CURRENT_TIMES');

# ----
# -- Table structure for Companies
# ----
# CREATE TABLE 'Companies' (
# 	'id'          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
# 	'name'        TEXT,
# 	'url'         TEXT  UNIQUE,
# 	'last_update' DATETIME DEFAULT CURRENT_TIMES
# 	);

# ----
# -- Data dump for Companies, a total of 3 rows
# ----
# INSERT INTO "Companies" ("id","name","url","last_update") VALUES ('1','Penn','https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/','CURRENT_TIMES');
# INSERT INTO "Companies" ("id","name","url","last_update") VALUES ('2','Comcast','https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers/jobs','CURRENT_TIMES');
# INSERT INTO "Companies" ("id","name","url","last_update") VALUES ('3','Brookings Institute','https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078','CURRENT_TIMES');

# ----
# -- Table structure for Job_User_Keywords
# ----
# CREATE TABLE 'Job_User_Keywords' (
#     'id'              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     'keyword'         TEXT,
#     'user_id'         INTEGER NOT NULL,
#     'case_sensitive'  BOOLEAN DEFAULT 'false',
#     'last_update'     DATETIME DEFAULT CURRENT_TIMESTAMP,
#     UNIQUE (`user_id`, `keyword`),
#     FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE
# );

# ----
# -- Data dump for Job_User_Keywords, a total of 3 rows
# ----
# INSERT INTO "Job_User_Keywords" ("id","keyword","user_id","case_sensitive","last_update") VALUES ('1','Data','1','false','2024-06-17 19:02:26');
# INSERT INTO "Job_User_Keywords" ("id","keyword","user_id","case_sensitive","last_update") VALUES ('2','Analyst','1','false','2024-06-17 19:03:41');
# INSERT INTO "Job_User_Keywords" ("id","keyword","user_id","case_sensitive","last_update") VALUES ('3','Research','1','false','2024-06-17 19:03:54');

# ----
# -- Table structure for User_Companies
# ----
# CREATE TABLE 'User_Companies' (
#        'id'         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#        'user_id'    INTEGER NOT NULL,
#        'company_id' INTEGER NOT NULL,
#        FOREIGN KEY (user_id)    REFERENCES Users (id) ON DELETE CASCADE,
#        FOREIGN KEY (company_id) REFERENCES Companies (id) ON DELETE CASCADE,
#        UNIQUE ('user_id', 'company_id')
# );

# ----
# -- Data dump for User_Companies, a total of 3 rows
# ----
# INSERT INTO "User_Companies" ("id","user_id","company_id") VALUES ('1','1','1');
# INSERT INTO "User_Companies" ("id","user_id","company_id") VALUES ('2','1','2');
# INSERT INTO "User_Companies" ("id","user_id","company_id") VALUES ('3','1','3');

# ----
# -- Table structure for Job_Entries
# ----
# CREATE TABLE 'Job_Entries' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
# 							'title' TEXT, 
# 							'url' TEXT , 
# 							'company_id' INTEGER, 
# 							'last_update' DATETIME DEFAULT CURRENT_TIMESTAMP, 
# 							UNIQUE (`company_id`, `title`, `url`), 
# 							FOREIGN KEY (company_id) REFERENCES Companies (id) );

# ----
# -- Data dump for Job_Entries, a total of 0 rows
# ----

# COMMIT;
               
#                """)