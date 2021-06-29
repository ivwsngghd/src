# -*- coding: utf-8-unix -*-

import os
import argparse
from flask import request, session, render_template, make_response, Blueprint, jsonify, redirect, url_for
import json
import random
import itertools
import requests
from jwcrypto.jwt import JWT, JWKSet
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from models import db, User


bp = Blueprint('auth', __name__, url_prefix='/api/auth')


ISSUER = 'https://i-oa.gzuni.com/open/'
CLIENT_ID = 'test'
CLIENT_SECRET = ''

CALLBACK_URL = 'http://localhost:5000/api/auth/callback'

conf = {}


def load_op_conf(issuer):
    issuer = issuer.rstrip('/')
    if issuer in conf:
        return conf[issuer]
    url = issuer + '/.well-known/openid-configuration'
    resp = requests.get(url)
    rs = json.loads(resp.text)
    conf[issuer] = rs
    return rs


def _ord(c):
    if isinstance(c, int):
        return c
    return ord(c)


def rndstr(size):
    if size <= 0:
        return ''
    elif size > 1024:
        size = 1024
    sample = [chr(c) for c in itertools.chain(
        [_ord('A')+i for i in range(26)],
        [_ord('a')+i for i in range(26)],
        [_ord('0')+i for i in range(10)],
    )]
    l = len(sample)
    rbytes = [_ord(r) for r in os.urandom(size)]
    return ''.join([sample[int(r * l/256.0)] for r in rbytes])


def get_remote_keyset(issuer):
    cfg = load_op_conf(ISSUER)
    j = requests.get(cfg['jwks_uri']).text
    kset = JWKSet.from_json(j)
    return kset


@bp.route('/oaLogin/')
def login():
    if 'id_token' in session:
        return jsonify({
            'is_login': True,
            'user': session['user'],
        })
    cfg = load_op_conf(ISSUER)
    state, nonce = rndstr(8), rndstr(8)
    args = {
        'response_type': 'id_token',
        'scope': '',
        'client_id': CLIENT_ID,
        'state': state,
        'nonce': nonce,
        'redirect_uri': CALLBACK_URL,
    }
    login_url = cfg['authorization_endpoint'] + '?' + urlencode(args)
    return jsonify({'is_login': False, 'url': login_url})


@bp.route('/callback', methods=['GET', 'POST'])
def oauth2_callback():
    cfg = load_op_conf(ISSUER)
    args = request.args
    if request.method == 'POST':
        args = request.form
    id_token_raw = args['id_token']
    prev_state = args['state']
    keyset = get_remote_keyset(ISSUER)
    id_token = JWT()
    id_token.deserialize(id_token_raw, key=keyset)
    userinfo_uri = cfg['userinfo_endpoint']
    resp = requests.get(userinfo_uri, headers={
        'Authorization': 'Bearer %s' % id_token_raw
    })
    user = json.loads(resp.text)
    session['id_token'] = id_token_raw
    session['user'] = user
    return '登录成功，正在跳转至首页...'


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'id_token' in session:
        session.pop('id_token', None)
        session.pop('user')
    return ('', 204)
