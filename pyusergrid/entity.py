# -*- coding: utf-8 -*-

from .resource import Resource


class Entity(Resource):

    def __init__(self, path, headers=None, response=None, index=None):
        self.index = index
        super(Entity, self).__init__(path, headers, response)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __str__(self):
        return str({self.path: self.data})

    @property
    def data(self):
        if not self.response:
            self.get()
        return self.response.entities_data[self.index] if self.index else self.response.entity_data

    def save(self):
        self.put(self.data)
