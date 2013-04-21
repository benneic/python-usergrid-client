# -*- coding: utf-8 -*-

from response import Response

import os
import requests
import utils


class Resource(object):

    API_URL = 'https://api.usergrid.com'

    HEADERS = {
        'content-type': 'application/json'
    }

    def __init__(self, path=API_URL, headers=None, entity=None):
        self.path = path
        self.headers = headers or Resource.HEADERS
        self.entity = entity

    def __getattr__(self, item):
        path = os.path.join(self.path, item)
        return Resource(path)

    def __repr__(self):
        return '{}<{}>'.format(__name__, self.path)

    def __str__(self):
        return unicode({self.path: self.entity})

    @property
    def access_token(self):
        return self.headers.get('Authorization', '').rsplit('Bearer ') or None

    @access_token.setter
    def access_token(self, value):
        self.headers.update({'Authorization': 'Bearer {}'.format(value)})

    @access_token.deleter
    def access_token(self):
        self.headers.pop('Authorization', None)

    def get(self, **params):
        response = requests.get(self.path, params=params, headers=self.headers)
        self.response = Response(self, response)
        self.response.raise_if_error()
        return self.response

    def post(self, data=None, **params):
        data = utils.jsonify_data(data)
        response = requests.post(self.path, data=data, params=params, headers=self.headers)
        self.response = Response(self, response)
        self.response.raise_if_error()
        return self.response

    def put(self, data=None, **params):
        data = utils.jsonify_data(data)
        response = requests.put(self.path, data=data, params=params, headers=self.headers)
        self.response = Response(self, response)
        self.response.raise_if_error()
        return self.response

    def delete(self, **params):
        response = requests.delete(self.path, params=params, headers=self.headers)
        self.response = Response(self, response)
        self.response.raise_if_error()
        return self.response

    def query(self, query=None, options=None):
        options = options or {}
        if query:
            options = options.update({'ql': query})
        return self.get(**options)

    def update_query(self, updates, query=None, options=None):
        options = options or {}
        if query:
            options = options.update({'ql': query})
        return self.put(data=updates, **options)

    def login(self, username, password):
        entity = self['token'].get(grant_type='password', username=username, password=password)
        self.access_token = entity['access_token']

    def save(self):
        self.put(self.entity)

    @property
    def entities(self):
        for entity in self.response.entities:
            yield Resource(entity['uri'], self.headers, entity=entity)
