from source.database.db_connect import mydb
from variables.path import path_dir
import select_quries

myCursor = mydb.cursor()


def delete_by_year_month(year_month):
    location = path_dir + 'delete_by_year_month.sql'

    with open(location, 'r') as file:
        query = file.read()
        file.close()
    try:
        myCursor.execute(query.format(year_month))
        mydb.commit()
        return 'Success'
    except Exception as e:
        print(e)


print(delete_by_year_month(202202))
print(select_quries.select_everything())

