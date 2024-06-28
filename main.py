from datetime import date
# Custom modules
import sendmail
import methods
import database

## Main Loop

# Update job_listings db
methods.penn_job_update() # ID 1
methods.comcast_job_update() # ID 2
methods.brookings_job_update() # ID 3

# Send emails to users
userid_list = database.get_userids()
user_emails = [x[1] for x in userid_list]

for u_id in [x[0] for x in userid_list]:
    todays_date = date.today()
    user_keywords = database.get_userkeywords(u_id)
    user_companies = database.get_usercompanies(u_id)
    company_names = [x[1] for x in user_companies]
    html = ['<html><body>',
            f'<h1>Job Report {todays_date}</h1>',
            '<p>Today\'s Job Report is as follows:</p>'
            ]
    for c_id in [x[0] for x in user_companies]:
            job_tuples = database.get_recentjobs(c_id, user_keywords)
            html.append(f'<h2>{company_names[c_id - 1]}</h2>')
            if job_tuples == []:
                  html.append('<p>No Jobs Found Matching Keywords</p>')
            else:
                for i in job_tuples:
                    html.append(f'<a href={i[1]}>{i[0]}</a><br />')
    html.append('</body></html>')
    sendmail.email_send(user_emails[u_id - 1], ''.join(html))

