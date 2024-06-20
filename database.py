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

