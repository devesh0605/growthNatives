import mysql.connector
from variables import creds

h = creds.shost
u = creds.suser
p = creds.spasswd
d = creds.sdatabase
mydb = mysql.connector.connect(host=h, user=u, passwd=p, database=d)
