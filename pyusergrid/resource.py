# -*- coding: utf-8 -*-

import os
import requests

DEFAULT_API_URL = 'https://api.usergrid.com'

HEADERS = {
    'content-type': 'application/json'
}


class Resource(object):

    def __init__(self, path=DEFAULT_API_URL, headers=None, response=None):
        self.path = path
        self.headers = headers or HEADERS
        self.response = response

    def __getitem__(self, item):
        path = os.path.join(self.path, item)
        return Resource(path)

    def __repr__(self):
        return '{}<{}>'.format(__name__, self.path)

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
        return Response(self, response)

    def post(self, data=None, **params):
        response = requests.get(self.path, data=data, params=params, headers=self.headers)
        return Response(self, response)

    def put(self, data=None, **params):
        response = requests.put(self.path, data=data, params=params, headers=self.headers)
        return Response(self, response)

    def delete(self, **params):
        response = requests.delete(self.path, params=params, headers=self.headers)
        return Response(self, response)

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
        response = self['token'].get(grant_type='password', username=username, password=password)
        self.access_token = response.data['access_token']
        return response
