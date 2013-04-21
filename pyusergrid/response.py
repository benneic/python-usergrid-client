# -*- coding: utf-8 -*-

from .errors import UsergridResponseError

import os
from datetime import datetime


class Response(object):

    def __init__(self, resource, response):
        self.resource = resource
        self.response = response
        self.data = response.json()

    @property
    def duration(self):
        return self.data['duration']

    @property
    def timestamp(self):
        return datetime.utcfromtimestamp(self.data['timestamp'])

    @property
    def error(self):
        return self.data.get('error')

    @property
    def error_description(self):
        return self.data.get('error_description')

    @property
    def exception(self):
        return self.data.get('exception')

    @property
    def action(self):
        return self.data.get('action')

    @property
    def application_name(self):
        return self.data.get('applicationName')

    @property
    def application_uuid(self):
        return self.data.get('application')

    def entities(self):
        for entity in self.data.get('entities', []):
            if isinstance(entity, dict) and entity.get('uuid'):
                entity['uri'] = os.path.join(self.uri, entity['uuid'])
            yield entity

    @property
    def organization(self):
        return self.data.get('organization')

    @property
    def params(self):
        return self.data.get('params')

    @property
    def path(self):
        return self.data.get('path')

    @property
    def uri(self):
        return self.data.get('uri')

    def raise_if_error(self):
        if not self.error:
            return
        raise UsergridResponseError(self)


