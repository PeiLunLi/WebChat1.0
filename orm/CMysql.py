import pymysql
import config

def singleton(cls, *args, **kwargs):
  instances = {}
  def _singleton():
    if cls not in instances:
      instances[cls] = cls(*args, **kwargs)
    return instances[cls]
  return _singleton

@singleton
class CMySQL():
    host = config.mysql["host"]
    user = config.mysql["user"]
    passwd = config.mysql["passwd"]
    dbName = config.mysql["dbName"]

    def connet(self):
        self.db = pymysql.connect(self.host, self.user, self.passwd, self.dbName)
        self.cursor = self.db.cursor()
    def close(self):
        self.cursor.close()
        self.db.close()

    def get_one(self, sql):
        res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except:
            print("查询失败")
        return res



    def get_all(self, sql):
        res = ()
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except:
            print("查询失败")
        return res
        # (("tom",18,100),(),())

    def get_all_obj(self, sql, tableName, *args):
        resList = []
        fieldsList = []
        if (len(args) > 0):
            for item in args:
                fieldsList.append(item)
        else:
            fieldsSql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'" % (
            tableName, self.dbName)
            fields = self.get_all(fieldsSql)
            for item in fields:
                fieldsList.append(item[0])

        #执行查询数据sql
        res = self.get_all(sql)
        for item in res:
            obj = {}
            count = 0
            for x in item:
                obj[fieldsList[count]] = x
                count += 1
            resList.append(obj)
        return resList
        # [{"name":"tom","age":18},{}]



    def insert(self, sql):
        return self.__edit(sql)
    def update(self, sql):
        return self.__edit(sql)
    def delete(self, sql):
        return self.__edit(sql)
    def __edit(self,sql):
        count = 0
        try:
            self.connet()
            count = self.cursor.execute(sql)
            self.db.commit()

            self.close()
        except :
                print("事物提交失败")
                self.db.rollback()
        return count