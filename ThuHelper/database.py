from bae.core import const
import MySQLdb
from django.http import HttpResponse
def testTable(request):
    dbname = "JeeyjPsbXniwEMCMuloW"
    mydb = MySQLdb.connect(
        host = const.MYSQL_HOST,
        port = int(const.MYSQL_PORT),
        user = const.MYSQL_USER,
        passwd = const.MYSQL_PASS,
        db = dbname,
    )
    cursor = mydb.cursor()
    cursor.execute('Select * from classroom')
    classrooms = [row[1] for row in cursor.fetchall()]
    for room in classrooms:
        print(room)
    mydb.close()
    return HttpResponse(classrooms[0])

def