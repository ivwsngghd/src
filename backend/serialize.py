from flask.json import JSONEncoder as _JSONEncoder

# from app.libs.error_code import ServerError
from datetime import date


# 自定义的json序列化器，然后在app.py配置，替换掉默认的json序列化器
class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            if isinstance(o, list):
                return [dict(x) for x in o]
            else:
                return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        # raise ServerError
