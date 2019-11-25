#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: bingweichen
@contact: bingwei.chen11@gmail.com
@File    : base_service.py
@Time    : 2019/11/18 2:10 PM
@Site    : 
@Software: IntelliJ IDEA
@desc: 
"""


class BaseService:
    def __init__(self, cls):
        self.cls = cls

    def get_all(self):
        return self.cls.query.filter_by().all()

    def get_all_json(self):
        objs_json = []
        objects = self.get_all()
        for obj in objects:
            obj_dict = obj.as_dict()
            objs_json.append(obj_dict)
        return objs_json