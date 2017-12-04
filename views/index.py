from tornado import escape
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
import tornado.web

from models import user,groups,user_group,user_user

#主页
class HomeHandler(RequestHandler):

    def get(self, *args, **kwargs):
        '''
        获取主页
        '''
        self.render('chat_online.html')

#注册
class RegisterHandler(RequestHandler):
    
    def get(self, *args, **kwargs):
        '''
        返回注册页
        '''
        self.render('register.html')
        
    def post(self, *args, **kwargs):
        '''
        提交注册
        '''
        stus =user.all()
        name = self.get_argument('name')
        userid = self.get_argument('user')
        passwd = self.get_argument('passwd')
        passwd2 = self.get_argument('passwd2')
        for stu in stus:
            if str(stu['user']) == userid or name == None or userid ==None or passwd == None or passwd != passwd2:
                print('wrrong')
                self.redirect('/register')
                break
            else:
                print('ok')
                print(name,userid,passwd)
                stu = user(userid, passwd,name)
                stu.save()
                self.redirect('/login')
                break
                
#登陆验证
class LoginHandler(RequestHandler):
    
    def get(self, *args, **kwargs):
        next = self.get_argument('next','/')
        url = '/login?next=' + next
        self.render('login.html',url=url)
        
    def post(self, *args, **kwargs):
        name = self.get_argument('username')
        passwd = self.get_argument('passwd')
        stus = user.all()
        for stu in stus:
            if str(stu['user']) == str(name):
                if str(stu['passwd']) == passwd:

                    self.set_cookie('user', str(stu['user']))

                    next = self.get_argument('next', '/')
                    if next == '/':
                        self.redirect('/chatromshow')
                        break
                    else:
                        self.redirect(next+'?flag=logined')
                        break
                else:
                    next = self.get_argument('next', '/')
                    self.redirect('/login?next-' + next)
                    break






#聊天室
class ChatRomShowHandler(RequestHandler):
    def get_current_user(self):
        '''
        获取当前用户
        '''
        flag = self.get_argument("flag", None)
        _cookie = self.get_cookie("user",None)
        # print(_cookie)
        if flag or _cookie:
            return True
        
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        '''
        渲染页面
        '''
        chat_with_id = self.get_argument('user_id',None)
        chat_group_id = self.get_argument('group_id', None)

        self.cookie = int(self.get_cookie('user'))

        user_detail =user.filter(user =self.cookie)[0]
        frinds = user_user.filter(user_id = self.cookie)

        quanzi = user_group.filter(user_id=user_detail['user'])
        if chat_with_id :
            chat_with = user.filter(user =int(chat_with_id))[0]
            self.set_cookie('chat_id', chat_with_id)
            self.set_cookie('change', 'one')
        elif chat_group_id:
            _dic = groups.filter(number=int(chat_group_id))[0]
            chat_with = {'name': _dic['name'], 'id': _dic['id'], 'user':_dic['number']}
            self.set_cookie('group_id', str(_dic['number']))
            self.set_cookie('change', 'many')
            #[{'id': 1, 'group_id': 1000, 'user_id': 200}]
            # chat_with = user.filter(user=int(_dic['user_id']))
        else:
            chat_with ={ 'name': '自己', 'id': 1, 'user': 100}
        frinds_list = []
        groups_list = []
        for frind in frinds:

            _id=frind['frinds_id']
            frind_detail = user.filter(user=_id)[0]
            frinds_list.append(frind_detail)

        for quan in quanzi:

            _id=quan['group_id']
            group_detail = groups.filter(number=int(_id))[0]
            groups_list.append(group_detail)


        stus = {
            #{'passwd': '101', 'name': '121', 'id': 10, 'user': 1}
            'user_detail':user_detail,
            #[{'name': 'a', 'passwd': '123', 'id': 1, 'user': 100}]
            'frinds':frinds_list,
            #[{'name': 'gr', 'id': 1, 'number': 1000}]
            'groups':groups_list,
            'chat_with':chat_with,
        }

        self.render('chat_rom.html',stus = stus)

        
class ChatStartHandler(WebSocketHandler):
    users = []

    def open(self, *args, **kwargs):
        '''
        当建立连接
        '''
        # 将登陆的用户存储到用户列表
        self.users.append(self)
        self.cookie = self.get_cookie('user')
        self.chat_id = []
        if self.get_cookie('change') == 'one':
            self.chat_id2 =self.get_cookie('chat_id')
            self.chat_id.append(self.chat_id2)
        else:


            chat_id = self.get_cookie('group_id')
            chat_id = user_group.filter(group_id=int(chat_id))

            for num in chat_id:
                self.chat_id.append(num['user_id'])

        for chat in self.chat_id:
            for u in self.users:
                if u.cookie == str(chat):
                    print('有人接入')
                    name = user.filter(user = int(u.cookie ))[0]['name']
                    u.write_message("[%s]开始聊天" % (name))

    def on_close(self):
        '''
        当关闭
        '''
        self.users.remove(self)
        for chat in self.chat_id:
            for u in self.users:
                if u.cookie == str(chat):
                    print('有人断开连接')
                    name = user.filter(user=int(u.cookie))[0]['name']
                    u.write_message("[%s]离开聊天" % (name))

    def on_message(self, message):
        '''
        当发消息
        '''
        for chat in self.chat_id:
            for u in self.users:
                cookiess = u.get_cookie('user')
                if str(cookiess) == str(chat):
                    print('服务器收到一条消息')
                    name = user.filter(user=int(self.cookie))[0]['name']
                    u.write_message("[%s]说：%s" % (name, message))


    def check_origin(self, origin):
        # 允许WebSocket的跨域请求
        return True

#添加
class AddFrindHandler(RequestHandler):
    def get(self, *args, **kwargs):
        '''
        添加好友
        '''
        user_id = self.get_cookie('user')
        frinds_id = self.get_argument("number", None)
        stu = user_user(user_id, frinds_id)
        stu.save()
        stu2 = user_user(frinds_id,user_id)
        stu2.save()
        self.redirect('/chatromshow')

class AddGroupHandler(RequestHandler):
    def get(self, *args, **kwargs):
        '''
        添加群
        '''
        user_id = self.get_cookie('user')
        group_id = self.get_argument("number", None)
        stu2 = user_group(group_id,user_id)
        stu2.save()
        self.redirect('/chatromshow')




#聊天
class ShowChatHandler(RequestHandler):
    def get_current_user(self):
        '''
        获取当前用户
        '''
        flag = self.get_argument("flag", None)
        _cookie = self.get_cookie("user",None)
        if flag or _cookie:
            return True
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('chat.html')


class ChatHandler(WebSocketHandler):
    users = []

    def open(self, *args, **kwargs):
        #将登陆的用户存储到用户列表

        self.cookie =self.get_cookie('user')
        # print(cookie)
        self.users.append(self)
        for u in self.users:
            u.write_message("[%s]登陆聊天室"%(self.cookie))
    def on_close(self):
        '''
        关闭聊天室
        '''
        self.users.remove(self)
        for u in self.users:
            u.write_message("[%s]离开聊天室"%(self.request.remote_ip))
    def on_message(self, message):
        '''
        发消息
        '''
        for u in self.users:
            u.write_message("[%s]说：%s"%(self.cookie, message))
    def check_origin(self,origin):
        #允许WebSocket的跨域请求
        return True
