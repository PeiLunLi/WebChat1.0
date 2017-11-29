import tornado.web
import config
from views import index
class Application(tornado.web.Application):
    def __init__(self):
        urls ={
            #主页
            (r'/home',index.HomeHandler),
            #用户验证
            (r'/login',index.LoginHandler),
            (r'/register', index.RegisterHandler),
            #聊天
            (r'/showchat', index.ShowChatHandler),
            (r'/chat', index.ChatHandler),
            #聊天室
            (r'/chatromshow', index.ChatRomShowHandler),
            (r'/chatstart',index.ChatStartHandler),
            #添加
            (r'/frind', index.AddFrindHandler),
            (r'/group', index.AddGroupHandler),

        }
        super(Application,self).__init__(urls,**config.settings)