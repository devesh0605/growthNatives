from source.database.db_connect import mydb
from variables.path import path_dir

myCursor = mydb.cursor()


def insert_new_query(ga_year_month, ga_users, ga_bounce_rate, display_ga_users, display_ga_bounce_rate, direct_ga_users,
                     direct_ga_bounce_rate, paid_search_ga_users, paid_search_ga_bounce_rate, organic_search_ga_users,
                     organic_search_ga_bounce_rate, referral_ga_users, referral_ga_bounce_rate, social_ga_users,
                     social_ga_bounce_rate, other_ga_users, other_ga_bounce_rate, email_ga_users, email_ga_bounce_rate):
    location = path_dir + 'insert_new_record.sql'

    with open(location, 'r') as file:
        query = file.read()
        file.close()
    try:
        myCursor.execute(query.format(ga_year_month, ga_users, ga_bounce_rate, display_ga_users, display_ga_bounce_rate,
                                      direct_ga_users,
                                      direct_ga_bounce_rate, paid_search_ga_users, paid_search_ga_bounce_rate,
                                      organic_search_ga_users,
                                      organic_search_ga_bounce_rate, referral_ga_users, referral_ga_bounce_rate,
                                      social_ga_users,
                                      social_ga_bounce_rate, other_ga_users, other_ga_bounce_rate, email_ga_users,
                                      email_ga_bounce_rate))
        mydb.commit()
        return 'Success'
    except Exception as e:
        print(e)


print(insert_new_query('202204', '1334.0', '80.53880176919984', '749.0', '86.01190476190477', '187.0',
                       '65.2542372881356', '151.0',
                       '70.4035874439462', '200.0', '72.42647058823529', '22.0', '40.0', '15.0',
                       '87.09677419354838', '10.0',
                       '90.0',
                       '0.0', '0.0'))
