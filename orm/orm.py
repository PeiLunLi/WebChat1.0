from orm.CMysql import  CMySQL

class ORM():
    def save(self):
        tableName = (self.__class__.__name__).lower()
        fieldStr = "("
        valueStr = "("
        for field in self.__dict__:
            fieldStr += (field + ",")
            if isinstance(self.__dict__[field], str):
                valueStr += ("'" + self.__dict__[field] + "',")
            else:
                valueStr += (str(self.__dict__[field]) + ",")
        fieldStr = fieldStr[:len(fieldStr) - 1] + ")"
        valueStr = valueStr[:len(valueStr) - 1] + ")"
        sql = "insert into " + tableName + " " + fieldStr + " values" + valueStr
        # print(sql)
        db = CMySQL()
        db.insert(sql)

    def delete(self):
        pass

    @classmethod
    def all(cls):
        # select * from students
        tableName = (cls.__name__).lower()
        sql = "select * from " + tableName
        db = CMySQL()
        return db.get_all_obj(sql, tableName)

    @classmethod
    def filter(cls,**kwargs):
        for key in kwargs:
            contex_key = key
        stus = cls.all()

        result_list = []

        for line in stus:

            for key in line:
                if key == contex_key:

                    if line[key] == kwargs[contex_key]:
                        # print(line[key], type(line[key]), kwargs[contex_key], type(kwargs[contex_key]))
                        result_list.append(line)
        return result_list