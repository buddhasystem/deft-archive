from django.db import connection

def getSeq(): # to be fixed later... temp way to get the seq number...
    cursor = connection.cursor()
    cursor.execute("select ATLAS_DEFT.PRODSYS2_TASK_ID_SEQ.nextval from dual connect by level<2")
    row = cursor.fetchone()
    return str(row[0])
