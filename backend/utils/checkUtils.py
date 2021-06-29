from flask import json

# 需要注意字段的定义
from models import Package


# 用来检测分页等相关信息的
def paging_check(params, model):
    order = model.id.asc()  # 默认id排序 排序方式
    cur_page = 1  # 默认值 当前页码
    per_page = 20  # 默认值 当前内容条数
    if 'current' in params:
        if (params['current']).isdigit():
            cur_page = int(params['current'])
        del params['current']
    if 'pageSize' in params:
        if (params['pageSize']).isdigit():
            per_page = int(params['pageSize'])
        del params['pageSize']
    if 'sorter' in params:
        sorter = json.loads(params['sorter'])
        del params['sorter']
        if sorter:
            try:
                order = getattr(model, next(iter(sorter)))
                order = order.asc() if next(iter(sorter.items()))[
                                           1] == 'ascend' else order.desc()
            except AttributeError:  # 排序格式有误
                error_code = 1
                # pass
    return params, cur_page, per_page, order


# 检测包添加删除资产的参数问题
def check_id(params):
    _id = None
    error_code = 0  # 默认值 错误代码
    error_msg = ""
    success = True
    try:
        _id = int(params['id'])
    except (TypeError, ValueError, KeyError):
        error_code = 1
        error_msg = '传入参数格式有误'
        success = False
    return _id, success, error_code, error_msg
