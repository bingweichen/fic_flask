#!/usr/bin/env python
# -*- coding: utf-8 -*-
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