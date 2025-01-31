from __future__ import annotations
import apsw
import apsw.ext
import apsw.bestpractice
import itertools

apsw.bestpractice.apply(apsw.bestpractice.recommended)

connection = apsw.Connection("job_listings.sqlite3")
cursor = connection.cursor()

company_name = 'Drexel'
company_url = 'https://careers.drexel.edu/en-us/listing/'
users_associated = [1, 2]

def create_company_id(company_name, company_url):
    company_id = cursor.execute(
        "INSERT INTO Companies ('name', 'url')"
        f"    VALUES ('{company_name}','{company_url}')"
        "     RETURNING Companies.id"
    ).get
    return company_id

def add_user_companies(users_associated, company_id):
    data = [[*t] for t in zip(users_associated, itertools.repeat(company_id))]
    query = (
        "INSERT INTO User_Companies ('user_id', 'company_id')"
        f"     VALUES (?, ?)"
    )
    cursor.executemany(query, data)

def add_company(company_name, company_url, users_associated):
    company_id = create_company_id(company_name, company_url)
    add_user_companies(users_associated, company_id)
    print(f'Added Company: ID = {company_id}')

add_company(company_name, company_url, users_associated)