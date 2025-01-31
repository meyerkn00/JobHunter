from datetime import date
import time
# Custom modules
import methods.send_mail as send_mail
import methods.web_queries as web_queries
import methods.database as database

## Main Loop
# start = time.time()
# Update job_listings db
web_queries.update_job_db()

# Send get list of active users
active_users = database.get_userids()

# Send emails to those users
def main_loop(userid_dict):
    for u_id in list(userid_dict):
        todays_date = date.today()
        user_keywords = database.get_userkeywords(u_id)
        user_companies = database.get_usercompanies(u_id)
        company_names = [y[1] for y in user_companies]
        html = [
            '<html><body>',
            f'<h1>Job Report {todays_date}</h1>',
            '<p>Today\'s Job Report is as follows:</p>'
        ]
        for c_id in [z[0] for z in user_companies]:
                job_tuples = database.get_recent_jobs(c_id, user_keywords)
                html.append(f'<h2>{company_names[c_id - 1]}</h2>')
                html.append('<ul>')
                if job_tuples == []:
                    html.append("""
                            </ul>
                            <p>No Jobs Found Matching Keywords<p>
                            """)
                else:
                    for i in job_tuples:
                        html.append(f'<li><a href={i[1]}>{i[0]}</a><br /></li>')
                html.append('</ul>')
        html.append('</body></html>')
        send_mail.email_send(userid_dict[u_id], ' '.join(html))


if active_users != None:
     main_loop(active_users)
else:
     print("No active users, no mail sent")
# end = time.time()
# print(f'Time taken was {end-start} seconds')