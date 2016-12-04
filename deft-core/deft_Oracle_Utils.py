import sys

import time
from datetime import datetime

import cx_Oracle
from deft_Logger	import *

from dbaccess import dbaccess

################################################
class deft_Oracle:
    """Constructor"""
    def __init__(self, simu=False):
        self.meta_table		= 'DEFT_META'
        self.task_table		= 'DEFT_TASK'
        self.dataset_table	= 'DEFT_DATASET'
        self.task_seq		= 'DEFT_TASK_SEQ'
        self.comm		= 'PRODSYS_COMM'

        self.req_table		= 'DEFT_REQUEST'

        self.connection 	= None
        self.cursor		= None
        self.simu		= simu
        creds = dbaccess()
        
        self.db		= creds['default']['NAME']
        self.user	= creds['default']['USER']
        self.passwd	= creds['default']['PASSWORD']

        self.seq	= 'ATLAS_DEFT.PRODSYS2_TASK_ID_SEQ' # shared with JEDI; note that there is also a dev/dev seqence, ATLAS_PANDA.DEFT_TASK_SEQ

    ###
    def connect(self):
        self.connection = cx_Oracle.connect(self.user+'/'+self.passwd+'@'+self.db)

    ###
    def disconnect(self):
        self.connection.close()
        self.connection = None


    ###
    def create_cursor(self):
        self.cursor = self.connection.cursor()
        
    ###
    def delete_cursor(self):
        self.cursor.close()
        self.cursor = None

    ###
    def execute_cursor(self, sql, dct=None):
        result = None

        if self.simu==True and dct:
            print 'sql	:', sql
            print 'data	:', dct
            return result
        
        if dct:
            try:
                self.cursor.execute(sql, dct)
            except:
                return result
# For better debuggig, the following may be used:
#            except cx_Oracle.DatabaseError, exc:
#                error, = exc.args
#                print >> sys.stderr, "Oracle-Error-Code:", error.code
#                print >> sys.stderr, "Oracle-Error-Message:", error.message
                
        else:
            self.cursor.execute(sql)
            result = self.cursor.fetchall() # [0][0]

        return result

    ###
    def purge_meta_db(self, meta):
        self.connect()
        self.create_cursor()

        sql = "DELETE FROM "+self.meta_table
        if meta != '0': sql+=" WHERE META_ID='"+meta+"'"
        self.cursor.execute(sql)
        
        sql = "DELETE FROM "+self.task_table
        if meta != '0': sql+=" WHERE TASK_META='"+meta+"'"
        self.cursor.execute(sql)

        sql = "DELETE FROM "+self.dataset_table
        if meta != '0': sql+=" WHERE DATASET_META='"+meta+"'"
        self.cursor.execute(sql)
        
        self.delete_cursor()
        self.connection.commit()
        self.disconnect()

    ###
    def insert_meta_db(self, meta = None):
        if meta==None:
            return -1

        ts = self.get_utc_ts() # get the UTC timestamp
        
        meta['META_REQ_TS'] = ts[0]
        meta['META_UPD_TS'] = ts[0]


        self.connect()
        self.create_cursor()
        sql = "INSERT INTO " + self.meta_table + " VALUES (:META_ID, :META_NAME, :META_TEMPLATE, :META_STATE, :META_COMMENT, :META_REQ_TS, :META_UPD_TS, :META_REQUESTOR, :META_WORKINGGROUP, :META_MANAGER, :META_VO, :META_CLOUD, :META_SITE, :META_ISSUE, :META_PRODSOURCELABEL)"

        self.execute_cursor(sql, dct = meta)
        
        self.delete_cursor()
        self.connection.commit()
        self.disconnect()
        
        return 0
    ###
    def insert_task_db(self, tasks = []):

        for t in tasks:

            self.connect()
            self.create_cursor()
            
            ts = self.get_utc_ts() # get the UTC timestamp
            t['TASK_MODIFICATIONTIME'] = ts[0]

            self.execute_cursor("INSERT INTO " +
                                self.task_table +
                                " VALUES (:TASK_ID, :TASK_META, :TASK_USERNAME, :TASK_WORKINGGROUP, :TASK_MODIFICATIONTIME, :TASK_CLOUD, :TASK_SITE, :TASK_STATE, :TASK_PARAM, :TASK_TAG, :TASK_COMMENT, :TASK_VO, :TASK_TRANSUSES, :TASK_TRANSHOME, :TASK_TRANSPATH, :TASK_PROCESSINGTYPE, :TASK_CORECOUNT, :TASK_NAME, :TASK_RUNNUM, :TASK_TASKTYPE, :TASK_PRODSOURCELABEL, :TASK_ISSUE)",
                                dct = t)

            self.delete_cursor()
            self.connection.commit()
            self.disconnect()

    ###
    def fetch_task_db(self, task_id):
        self.connect()
        self.create_cursor()

        task = self.execute_cursor("SELECT * FROM "+self.task_table+" WHERE TASK_ID='"+task_id+"'")

        t = []
        for col in task[0]: # need to handle CLOB reading
            try:
                t.append(col.read())
            except:
                t.append(col)

        self.delete_cursor()
        self.disconnect()
        return t
        
    ###
    def insert_dataset_db(self, datasets = []):
        self.connect()
        self.create_cursor()

        for d in datasets: # see comment above regarding why we copy over
            insert_data = d

            self.execute_cursor("INSERT INTO " +
                                self.dataset_table +
                                " VALUES (:DATASET_ID, :DATASET_NAME, :DATASET_META, :DATASET_STATE, :DATASET_SOURCE, :DATASET_TARGET, :DATASET_COMMENT, :DATASET_FLAVOR, :DATASET_FORMAT, :DATASET_TOKEN, :DATASET_OFFSET)",  dct = insert_data)

        self.delete_cursor()
        self.connection.commit()
        self.disconnect()

    ###
    def retrieve_meta_db(self, meta_id):
        self.connect()
        self.create_cursor()

        tasks	= self.execute_cursor("SELECT * FROM "	+	self.task_table		+	" WHERE TASK_META='"	+	meta_id+"'")
        datasets= self.execute_cursor("SELECT * FROM "	+	self.dataset_table	+	" WHERE DATASET_META='"	+	meta_id+"'")

        self.delete_cursor()
        self.disconnect()
        return (tasks, datasets)
        
    ###
    def get_task_seq_db(self, cnt=1):

        v = [] # container for a vector of serial numbers
        
        self.connect()
        self.create_cursor()

        # simple single number extraction: seqno = self.execute_cursor("select ATLAS_PANDA.DEFT_TASK_SEQ.nextval from dual") 
        
        seq_vec = self.execute_cursor("select "+self.seq+".nextval from dual connect by level<"+str(cnt+1))

        for e in seq_vec: v.append(e[0])

        self.delete_cursor()
        self.connection.commit()
        self.disconnect()
        
        return v
    
    
    ###
    def get_utc_ts(self):
        self.connect()
        self.create_cursor()
        self.cursor.execute("ALTER SESSION SET TIME_ZONE='UTC'")
        db_datetime_tuple = self.execute_cursor("select CURRENT_DATE from dual")
        db_datetime = db_datetime_tuple[0][0]
        
        iso = db_datetime.isoformat(' ')
        ticks = int(time.mktime(db_datetime.timetuple()))
        return (db_datetime, iso, ticks)
    
    # example of initializing from an ISO string: datetime.strptime(iso, '%Y-%m-%d %H:%M:%S')

    ###
    def update_comm(self, message):

        insert_data = {}

        ts = self.get_utc_ts()

        insert_data['COMM_TASK']	= str(message['COMM_TASK'])
        insert_data['COMM_OWNER']	= str(message['COMM_OWNER'])
        insert_data['COMM_CMD']		= str(message['COMM_CMD'])
        insert_data['COMM_COMMENT']	= str(message['COMM_COMMENT'])

        insert_data['COMM_TS'] = ts[0]
        
        # print insert_data
        # print ts[0]
        
        self.connect()
        self.create_cursor()
        self.execute_cursor("INSERT INTO " + self.comm + " VALUES (:COMM_TASK, :COMM_OWNER, :COMM_CMD, :COMM_TS, :COMM_COMMENT)",
                                dct = insert_data)
        self.delete_cursor()
        self.connection.commit()
        self.disconnect()

    ###
    def update_req(self, req):
        insert_data = {}
        for k in req.keys():
            print k, req[k]
            if k=='REQID':
                insert_data[str(k)]=int(req[k])
            else:
                insert_data[str(k)]=str(req[k])

        print insert_data
        self.connect()
        self.create_cursor()
        self.execute_cursor("INSERT INTO " +
                            self.req_table +
                            " VALUES (:REQID, :MANAGER, :DESCRIPTION, :REFERENCE_LINK, :STATUS, :PROVENANCE, :REQTYPE, :CAMPAIGN, :SUBCAMPAIGN, :PHYSGROUP, :ENERGY)", dct = insert_data)
        self.delete_cursor()
        self.connection.commit()
        self.disconnect()
