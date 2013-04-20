# -*- coding: utf-8 -*-

from .entity import Entity

import os


class InvalidResponseError(Exception):
    pass


class Response(object):

    def __init__(self, resource, response):
        self.resource = resource
        self.response = response

    _entities_data = None
    _entities = None

    @property
    def data(self):
        return self.response.json()

    def has_multiple_entities(self):
        entities_data = self.data.get('entities') or self.data.get('data') or self.data.get('messages')
        return isinstance(entities_data, list)

    @property
    def entities_data(self):
        if self._entities_data:
            return self._entities_data
        entities_data = self.data.get('entities') or self.data.get('data') or self.data.get('messages') or self.data.get('list')
        if not isinstance(entities_data, list):
            raise InvalidResponseError('Unable to retrieve entities from response: %s', self.data)
        for entity in entities_data:
            if isinstance(entity, dict) and entity.get('uuid'):
                entity['uri'] = os.path.join(self.data['uri'], entity['uuid'])
        self._entities_data = entities_data
        return entities_data

    @property
    def entities(self):
        if not self._entities:
            self._entities = list()
            index = -1
            for d in self.entities_data:
                index += 1
                e = d if isinstance(d, list) else Entity(d['uri'], self.resource.headers, self, index)
                self._entities.append(e)
        return self._entities

    @property
    def entity_data(self):
        if self.has_multiple_entities():
            for entity in self.entities_data:
                return entity
        entity = self.data.get('data') or self.data.get('organization')
        if entity:
            entity = self.data.get('data')
            entity['uri'] = self.resource.path
            return entity
        for e in self.entities_data.values():
            return e

    @property
    def entity(self):
        entity_data = self.entity_data
        return Entity(entity_data['uri'], self.resource.headers, self) if entity_data else None


