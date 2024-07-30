from __future__ import annotations

from typing import Optional, Iterator, Any

import os
import sys
import time
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import apsw
import apsw.ext
import random
import re
import itertools
from pathlib import Path
import apsw.bestpractice


# # Checking APSW and Sqlite Versions
# # Where the extension module is on the filesystem
# print("      Using APSW file", apsw.__file__)

# # From the extension
# print("         APSW version", apsw.apsw_version())

# # From the sqlite header file at APSW compile time
# print("SQLite header version", apsw.SQLITE_VERSION_NUMBER)

# # The SQLite code running
# print("   SQLite lib version", apsw.sqlite_lib_version())

# # If True then SQLite is incorporated into the extension.
# # If False then a shared library is being used, or static linking
# print("   Using amalgamation", apsw.using_amalgamation)

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")
cursor = connection.cursor()

# Useful at startup to detect some database corruption
check = connection.pragma("integrity_check")
if check != "ok":
    print("Integrity check errors", check)

# Needed Queries

def add_to_jobs(company_id, datatable):
    data = [[*t] for t in zip(datatable['names'], datatable['links'], itertools.repeat(company_id))]
    query = """INSERT OR IGNORE INTO Job_Entries ("title", "url", "company_id")
                    VALUES (?, ?, ?)"""
    with connection:
        connection.executemany(query, data)

def get_userids():
    query = ('SELECT U.id, U.email FROM Users U'
                ' JOIN User_Companies UC ON (UC.user_id = U.id)'
                ' GROUP BY U.id'
                ' HAVING COUNT(UC.company_id) > 0')
    return cursor.execute(query).fetchall()

def get_userkeywords(user_id):
    query = ('SELECT keyword FROM Job_User_Keywords JUK'
                f' WHERE JUK.user_id = ?')
    return cursor.execute(query, (user_id,)).get

def get_usercompanies(user_id):
    query = ('SELECT UC.company_id, C.name FROM User_Companies UC'
                '  JOIN Companies C ON (C.id = UC.company_id)'
                f' WHERE UC.user_id = ?')
    return cursor.execute(query, (user_id,)).fetchall()

def keyword_list(keywords):
    list = []
    for k in keywords:
        if k == keywords[0]:
            list.append(f"'%{k}%'")
        else:
            list.append(f"OR JE.title LIKE '%{k}%'")
    return ' '.join(list)

def get_recent_jobs(company_id, keywords):
    # Note: update with FTS5 searching once I enable it
    one_week_ago = datetime.now(tz=timezone.utc) - timedelta(weeks = 1)
    one_week_ago_str = one_week_ago.strftime("%Y-%m-%d %H:%M:%S")
    query = ('SELECT JE.title, JE.url FROM Job_Entries JE'
            f' WHERE (JE.company_id = ?)'
            f' AND (JE.last_update > ?)'
            f' AND (JE.title LIKE {keyword_list(keywords)})'
            '  ORDER BY last_update DESC'
            '  LIMIT 10')
    result = cursor.execute(query, (company_id, one_week_ago_str)).fetchall()
    if result == None:
        return []
    else:
        return result