
from models import user
context = {
    'user':'123456'
}

a =user.filter(**context)
print(a)

