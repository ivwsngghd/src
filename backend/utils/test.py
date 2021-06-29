import pymysql
from flask import request, Blueprint, jsonify
from sqlalchemy import and_

from models import Package, db, Assets, packageAssetsAssoc
from utils.checkUtils import paging_check, check_id

bp = Blueprint('test', __name__, url_prefix='/api/test')


@bp.route('/test.do/', methods=['GET'])
def testapi():
    count = 0
    while count < 50:
        count += 1
        assets = Assets(batch_id=1, assets_id=count, assets_label='assetsLabel:' + str(count),
                        assets_name='assetsName:' + str(count), elements_comp='elementsComp233')
        db.session.add(assets)
    db.session.commit()

    return jsonify(success=True)


@bp.route('/test1.do/', methods=['GET'])
def testapi1():
    package = Package.query.get(233)
    assetsList = Assets.query.filter(Assets.id >= 1, and_(Assets.id <= 50)).all()
    for t in assetsList:
        package.assets.append(t)
    db.session.commit()
    return jsonify(success=True)


@bp.route('/test2.do/', methods=['GET'])
def testapi2():
    package = Package.query.get(233)
    create_date = package.create_date
    print(create_date)
    return jsonify(success=True, data=create_date)


@bp.route('/test3.do/', methods=['GET'])
def testapi3():
    package = {"id": "123123.1", "package_name": "23333name", "package_desc": "23333desc"}
    error_code, success, error_msg, id = check_id(package)
    return jsonify(success=success, error_msg=error_msg, error_code=error_code, id=id)
