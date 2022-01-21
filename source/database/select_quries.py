from source.database.db_connect import mydb
from variables.path import path_dir

myCursor = mydb.cursor()


def select_everything():
    location = path_dir + 'select_everything.sql'

    with open(location, 'r') as file:
        query = file.read()
        file.close()
    try:
        myCursor.execute(query)
        for i in myCursor:
            print(i)
        return 'Success'
    except Exception as e:
        print(e)


select_everything()
