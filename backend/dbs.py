from flask import Flask as _Flask
from serialize import JSONEncoder


class Flask(_Flask):
    json_encoder = JSONEncoder  # 使用自定义的JSON序列化器
