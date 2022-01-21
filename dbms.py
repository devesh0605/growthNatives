from source.database.db_connect import mydb

myCursor = mydb.cursor()
# val = ('202202', '1334.0', '80.53880176919984', '749.0', '86.01190476190477', '187.0', '65.2542372881356', '151.0',
#        '70.4035874439462', '200.0', '72.42647058823529', '22.0', '40.0', '15.0', '87.09677419354838', '10.0', '90.0',
#        '0.0', '0.0')
# myCursor.execute(sql, val)

# sql = "DELETE FROM analysis_data WHERE ga_yearMonth = '202202'"
# myCursor.execute(sql)

# mydb.commit()
try:
    myCursor.execute('select * from analysis_data')
    for i in myCursor:
        print(i)
except Exception as e:
    print(e)
