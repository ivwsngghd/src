import pymysql
from flask import request, Blueprint, jsonify
from flask_paginate import Pagination

from models import Package, db, Assets, Batch, Project
from utils.checkUtils import paging_check, check_id

bp = Blueprint('package', __name__, url_prefix='/api/package')


@bp.route('/list.do/', methods=['GET'])
def list_package():
    data = request.args.to_dict()
    error_code = 0
    data, cur_page, per_page, order = paging_check(data, Package)  # 参数校验
    if 'package_name' in data:  # 模糊查询
        query_set = Package.query.filter(Package.package_name.like("%" + data['package_name'] + "%")).order_by(
            order).paginate(
            page=cur_page, per_page=per_page,
            error_out=False, max_per_page=50)
    elif 'package_desc' in data:  # 模糊查询
        query_set = Package.query.filter(Package.package_desc.like("%" + data['package_desc'] + "%")).order_by(
            order).paginate(
            page=cur_page, per_page=per_page,
            error_out=False, max_per_page=50)
    else:
        query_set = Package.query.filter_by(**data).order_by(order).paginate(page=cur_page, per_page=per_page,
                                                                             error_out=False, max_per_page=50)
    return jsonify(data=query_set.items, success=True, total_pages=query_set.pages, error_code=error_code)


@bp.route('/create.do/', methods=['POST'])
def add_package():
    data = request.get_json()
    error_code = 0
    try:
        db.session.add(Package(**data))
        db.session.commit()
    except (pymysql.err.IntegrityError, Exception) as e:
        error_code = 1
        error_msg = '添加失败,请注意检查插入数据是否正确'
        return jsonify(error_code=error_code, error_msg=error_msg, succcess=False)
    return jsonify(error_code=error_code, error_msg="", succcess=True)


@bp.route('/detail.do/', methods=['GET'])
def package_detail():
    data = request.args.to_dict()
    data, cur_page, per_page, order = paging_check(data, Package)
    _id, success, error_code, error_msg = check_id(data)
    if success:
        package = Package.query.filter_by(id=_id, create_user='ivwsngghd').first()  # TODO 权限校验，私有package
        if package is None:
            return jsonify(error_code=error_code, error_msg='没有该资产包', success=False)
        assets_list = package.assets.paginate(page=cur_page, per_page=per_page,
                                              error_out=False, max_per_page=50).items
        project_name = None
        try:
            project_name = Batch.query.get(assets_list[0].batch_id).project.project_name
        except:
            pass
        result = {'package': package, 'assets_list': assets_list, 'project_name': project_name}  # 返回包，包内的资产列表，还有产品名字
        return jsonify(error_code=error_code, error_msg=error_msg, data=result, success=True)
    return jsonify(error_code=error_code, error_msg=error_msg, success=False)


@bp.route('/update.do/', methods=['POST'])
def update_package():
    data = request.get_json()
    query_res = Package.query.filter_by(id=data['id']).first()
    if query_res is None:
        return jsonify(success=False, error_msg='该包不存在，或参数有误')
    # TODO 这里能否修改status？
    query_res.set_attrs(data)
    db.session.commit()
    return jsonify(success=True)


@bp.route('/del.do/', methods=['POST'])
def delete_package():
    data = request.get_json()
    query_res = Package.query.filter_by(id=data['id']).first()
    if query_res is not None:
        # query_res.assets.all() 记得关联删除所有包里面的assets
        query_res.delete()
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, error_msg='该包不存在，或参数有误')


@bp.route('/package_assets_add.do/', methods=['POST'])
def assets_add_package():
    data = request.get_json()
    id_list = data['assets_id_list']  # 缺参数校验
    _id, success, error_code, error_msg = check_id(data)
    if success:
        query_res = Package.query.filter_by(id=_id).first()
    else:
        return jsonify(success=False, error_msg='传入参数有误')
    if query_res is None:
        return jsonify(success=False, error_msg='该包不存在')
    qs_list = Assets.query.filter(Assets.id.in_(id_list)).all()  # 部分id可能不存在
    qa_list = query_res.assets.all()
    for asset in qs_list:
        if asset not in qa_list:
            query_res.assets.append(asset)
    db.session.commit()
    return jsonify(success=True)


@bp.route('/package_assets_del.do/', methods=['POST'])
def assets_del_package():
    data = request.get_json()
    id_list = data['assets_id_list']  # 缺参数校验
    _id, success, error_code, error_msg = check_id(data)
    if success:
        query_res = Package.query.filter_by(id=_id).first()
    else:
        return jsonify(success=False, error_msg='传入参数有误')
    if query_res is None:
        return jsonify(success=False, error_msg='该包不存在')
    qs_list = Assets.query.filter(Assets.id.in_(id_list)).all()
    qa_list = query_res.assets.all()
    for asset in qs_list:
        if asset in qa_list:
            query_res.assets.remove(asset)
    db.session.commit()
    return jsonify(success=True)


@bp.route('/assets_search.do/', methods=['POST'])
def assets_search():
    data = request.get_json()
    print(data)
    return jsonify(success=True)