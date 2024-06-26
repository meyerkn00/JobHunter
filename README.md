# JobHunter
 Script for searching specific company job websites for new postings.

Uses SQL server to store results from previous days. Each time the script is run, it pulls jobs from the website and only adds the new entries to the DB. Then, for each User with related Companies, it pulls that company's jobs, filters it against the given keywords, and emails the result to the user.



# Dependencies
Written using python 3.12.3

- beautifulsoup4
- lxml
- pytest-playwright
    - then run 'playwright install'
- pandas
- jmapc
- apsw