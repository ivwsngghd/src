import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm
from datetime import datetime

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(2), nullable=False, default='0')  # REMOVE_TAG

    def __getitem__(self, item):
        return getattr(self, item)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


class User(Base):
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @orm.reconstructor
    def init_on_load(self):
        self.fields = ['username', 'email', 'ID', 'CREATE_DATE', 'status']


class Project(Base):
    __tablename__ = 'T_PROJECT'
    project_name = db.Column(db.String(80), unique=True, nullable=False)
    project_desc = db.Column(db.String(400))
    create_user = db.Column(db.String(40), nullable=False)
    project_status = db.Column(db.String(2), nullable=False, default='0')
    # batches = db.relationship("Batch", uselist=True, back_populates="T_PROJECT")
    batches = db.relationship("Batch", uselist=True, backref='project')

    # 配置用于返回的字段
    @orm.reconstructor
    def init_on_load(self):
        self.fields = ['id', 'project_name', 'project_desc', 'create_user',
                       'project_status', 'create_date', 'status']


class Batch(Base):
    __tablename__ = 'T_BATCH'
    batch_name = db.Column(db.String(200), nullable=False)
    planned_start_date = db.Column(db.DateTime)
    planned_end_date = db.Column(db.DateTime)
    actual_start_date = db.Column(db.DateTime)
    actual_end_date = db.Column(db.DateTime)
    batch_status = db.Column(db.String(2), nullable=False, default='0')
    project_id = db.Column(db.Integer, db.ForeignKey(
        'T_PROJECT.id'))

    # project = db.relationship('Project', back_populates="T_BATCH")

    @orm.reconstructor
    def init_on_load(self):
        self.fields = ['id', 'batch_name', 'planned_start_date', 'planned_end_date', 'project_id', 'project',
                       'create_date', 'status']

    # def __repr__(self):
    #     return '<batch_name %r batch_status %r>' % self.batch_name % self.batch_status


# 关联表关系建立
packageAssetsAssoc = db.Table('T_PACKAGE_DETAIL',
                              db.Column('id', db.Integer, primary_key=True),
                              db.Column('package_id', db.Integer, db.ForeignKey('T_PACKAGE.id')),
                              db.Column('assets_id', db.Integer, db.ForeignKey('T_ASSETS.id'))
                              )


class Package(Base):
    __tablename__ = 'T_PACKAGE'
    package_name = db.Column(db.String(200), nullable=False, unique=True)
    package_desc = db.Column(db.String(800))
    create_user = db.Column(db.String(40), nullable=False)
    assets = db.relationship('Assets', secondary=packageAssetsAssoc, back_populates='packages', lazy='dynamic')


    @orm.reconstructor
    def init_on_load(self):
        self.fields = ['id', 'package_name', 'package_desc', 'create_user', 'create_date']


class Assets(Base):
    __tablename__ = 'T_ASSETS'
    batch_id = db.Column(db.Integer, db.ForeignKey('T_BATCH.id'))
    assets_id = db.Column(db.String(400), name='col_key', nullable=False, unique=True)
    assets_label = db.Column(db.String(400), name='col_1')
    assets_name = db.Column(db.String(400), name='col_2')
    elements_comp = db.Column(db.String(2000), name='cols')
    # TODO
    packages = db.relationship('Package', secondary=packageAssetsAssoc, back_populates='assets', lazy='dynamic')

    @orm.reconstructor
    def init_on_load(self):
        self.fields = ['id', 'batch_id', 'assets_id', 'assets_label', 'assets_name', 'elements_comp']


class AssetsRight(Base):
    __tablename__ = 'T_ASSETS_RIGHT'
    user_id = db.Column(db.String(20), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('T_BATCH.id'))
    assets_id = db.Column(db.String(400), db.ForeignKey('T_ASSETS.col_key'), name='col_key')

    @orm.reconstructor
    def init_on_load(self):
        self.fields = ['user_id', 'batch_id', 'assets_id']

class AssetsInventory(Base):
    __tablename__ = 'T_ASSETS_INVENTORY'
    batch_id = db.Column(db.Integer, db.ForeignKey('T_BATCH.id'))
    assets_id = db.Column(db.String(400), db.ForeignKey('T_ASSETS.col_key'), name='col_key')
    inventory_status = db.Column(db.Integer, nullable=False, default='0')
    assets_balance_id = db.Column(db.String(400), name='local_01')
    assets_label = db.Column(db.String(400), name='local_02')
    assets_name = db.Column(db.String(400), name='local_03')
    assets_category = db.Column(db.String(400), name='local_04')
    category_desc = db.Column(db.String(400), name='local_05')
    elements_comp = db.Column(db.String(2000), name='cols')
    # TODO

    @orm.reconstructor
    def init_on_load(self):
        self.fields = ['id', 'batch_id', 'assets_id', 'inventory_status', 'assets_balance_id', 'assets_label', 'assets_name', 'assets_category', 'category_desc', 'elements_comp', 'create_date']
