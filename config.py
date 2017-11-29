import os
BASE_DIRS =os.path.dirname(__file__)

option ={
    'port':9999,
}

settings ={
    'template_path' : os.path.join(BASE_DIRS,'templates'),
    'static_path':os.path.join(BASE_DIRS,'static'),
    "debug": False,
    # "cookie_secret": "HTqWqcJpRA6Js2kPEQVIy9CvgddvPk1RhmsQMGmqzC8=",
    "login_url":"/login"


}
mysql ={
    'host':'127.0.0.1',
    'user':'root',
    'passwd':'111111',
    'dbName':'webchat01',
}