from orm import orm


class user(orm.ORM):
    def __init__(self, user, passwd,name):
        self.user = user
        self.passwd = passwd
        self.name = name
        
        
class groups(orm.ORM):
    def __init__(self, number,name):
        self.number = number
        self.name = name
        
        
class user_user(orm.ORM):
    def __init__(self, user_id, frinds_id):
        self.user_id = user_id
        self.frinds_id = frinds_id
        
        
class user_group(orm.ORM):
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
