# JobHunter
 Script for searching specific company job websites for new postings.

Uses SQL server to store results from previous days. Each time the script is run, it pulls jobs from the website and only adds the new entries to the DB. Then, for each User with related Companies, it pulls that company's jobs, filters it against the given keywords, and emails the result to the user.

File organization note: All of the important files are located within the app/ folder. Suggested deployment is to create a folder called Job Hunter. In that folder, place fastmail_key.txt, job_listings.sqlite3, and the app/ folder (also create a venv). When you want to run the script, call the following:

```~/JobHunter/.venv/bin/python ~/JobHunter/app/main.py```

# Dependencies
Written using python 3.12.3

- beautifulsoup4
- lxml
- pytest-playwright
    - then run 'playwright install'
- pandas
- jmapc
- apsw
For package versions, see requirements.txt