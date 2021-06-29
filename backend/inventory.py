from warnings import catch_warnings
from flask import request, session
from flask.blueprints import Blueprint
from flask.globals import current_app
from flask.json import jsonify
from requests.api import delete
from sqlalchemy.orm import query
from sqlalchemy.sql.elements import Null
from models import Batch, db, Project, Batch, Package
import json

from utils.checkUtils import paging_check

bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')


def pst(data, mod):
    for k in list(data):
        if data[k] == '':
            del data[k]

    offset = 0
    order = None

    if 'current' in data:
        offset = (int(data['current']) - 1) * int(data['pageSize'])
        del data['current']
        del data['pageSize']

    if 'sorter' in data:
        sorter = json.loads(data['sorter'])
        del data['sorter']
        if sorter:
            order = getattr(mod, next(iter(sorter)))
            order = order.asc() if next(iter(sorter.items()))[
                                       1] == 'ascend' else order.desc()

    return offset, order, data


@bp.route('/getProjects/', methods=['GET'])
def getProjects():
    data = request.args.to_dict()
    offset, order, data = pst(data, Project)
    query_set = Project.query.filter_by(
        **data).order_by(order).offset(offset).all() if order is not None else Project.query.filter_by(
        **data).order_by(Project.create_date.desc()).offset(offset).all()

    return jsonify(data=query_set, success=True, total=len(query_set))


@bp.route('/addProject/', methods=['POST'])
def addProject():
    data = request.get_json()
    pj = Project(**data)
    db.session.add(pj)
    db.session.commit()
    return jsonify(success=True)


@bp.route('/updateProject/', methods=['POST'])
def updateProject():
    data = request.get_json()
    query_res = Project.query.filter_by(id=data['id']).first()
    if query_res is not None:
        query_res.set_attrs(data)
        db.session.commit()
    return jsonify(success=True)


@bp.route('/removeProject/', methods=['DELETE'])
def removeProject():
    data = request.get_json()
    query_res = Project.query.filter_by(id=data['id']).first()
    if query_res is not None:
        db.session.delete(query_res)
        db.session.commit()
    return jsonify(success=True)


@bp.route('/removeProjects/', methods=['DELETE'])
def removeProjects():
    data = request.get_json()
    for item in data:
        try:
            Project.query.filter_by(id=item['id']).delete()
        except:
            pass
    db.session.commit()
    return jsonify(success=True)


@bp.route('/updateProjects/', methods=['POST'])
def updateProjects():
    data = request.get_json()
    for k in list(data[0]):
        if data[0][k] == '':
            del data[0][k]
    for item in data[1:]:
        try:
            query_res = Project.query.filter_by(id=item['id']).first()
            query_res.set_attrs(data[0])
        except:
            pass
    db.session.commit()
    return jsonify(success=True)


@bp.route('/getBatches/', methods=['GET'])
def getBatches():
    data = request.args.to_dict()

    offset, order, data = pst(data, Batch)

    query_set = Batch.query.filter_by(
        **data).order_by(order).offset(offset).all() if order is not None else Batch.query.filter_by(
        **data).order_by(Batch.create_date.desc()).offset(offset).all()

    return jsonify(data=query_set, success=True, total=len(query_set))


@bp.route('/addBatch/', methods=['POST'])
def addBatches():
    data = request.get_json()
    b = Batch(**data)
    db.session.add(b)
    db.session.commit()
    return jsonify(success=True)
