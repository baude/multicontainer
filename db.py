import pymysql

class DBDemo(object):
    def __init__(self, host, port):
        self.db = pymysql.connect(host,"root","x","DEMO" )
        self.cursor = self.db.cursor()

    def createtable(self):
        try:
            self.hasTable()
        except pymysql.err.ProgrammingError:
            sql = """CREATE TABLE NUMS(ID MEDIUMINT NOT NULL AUTO_INCREMENT, NUM FLOAT, PRIMARY KEY(ID))"""
            self.execute(sql)
            self.commit()

    def execute(self, sql):
        return self.cursor.execute(sql)

    def close(self):
        self.db.close()

    def commit(self):
        self.db.commit()

    def hasTable(self):
        sql = "SELECT * FROM NUMS"
        result = self.execute(sql)
        print(result)

    def getresultsfromid(self, id):
        c = self.db.cursor()
        sql = "SELECT * FROM NUMS WHERE ID > {}".format(id)
        c.execute(sql)
        return c.fetchall()
