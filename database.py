from __future__ import annotations

from typing import Optional, Iterator, Any

import os
import sys
import time
import datetime
import apsw
import apsw.ext
import random
import re
import itertools
from pathlib import Path
import apsw.bestpractice


# Checking APSW and Sqlite Versions
# Where the extension module is on the filesystem
print("      Using APSW file", apsw.__file__)

# From the extension
print("         APSW version", apsw.apsw_version())

# From the sqlite header file at APSW compile time
print("SQLite header version", apsw.SQLITE_VERSION_NUMBER)

# The SQLite code running
print("   SQLite lib version", apsw.sqlite_lib_version())

# If True then SQLite is incorporated into the extension.
# If False then a shared library is being used, or static linking
print("   Using amalgamation", apsw.using_amalgamation)

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")

# Useful at startup to detect some database corruption
check = connection.pragma("integrity_check")
if check != "ok":
    print("Integrity check errors", check)

# Needed Queries

def add_to_jobs(company_id, datatable):
    data = [zip(datatable['names'], datatable['links'], itertools.repeat(company_id), strict = True)]
    query = """INSERT INTO Job_Entries ("title", "url", "company_id")
                    VALUES (?, ?, ?)"""
    print(data)
    # connection.executemany(query, data)

# Pull company names
# def companylist():
#     list = []
#     for row in connection.execute("SELECT C.id FROM Companies C"):
#         list.append(row)
#     return list

# testing

# Test queries
# for row in connection.execute("""
#                 SELECT U.email, C.name, C.url FROM Users U  
#                     JOIN User_Companies UC ON (U.id = UC.user_id)  
#                     JOIN Companies C ON (UC.company_id = C.id)
#             """):
#     print(row)

# for row in connection.execute("select * from point"):
#     print(row)

# required for insert statements
# connection.execute("BEGIN")
# connection.execute()
# connection.execute("COMMIT")

# or

# with connection:
#     connection.execute()
#     connection.execute()
#     connection.execute()

def select_company_by_user(user_id):
    pass