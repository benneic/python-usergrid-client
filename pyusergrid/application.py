# -*- coding: utf-8 -*-

from . import Resource

import os


class Application(object):
    def __init__(self, organisation, application):
        path = '{}/{}'.format(organisation, application)
        path = os.path.join(Resource.DEFAULT_API_URL, path)
        self.app = Resource(path)
        self.users = self.app.users
        self.groups = self.app.groups
        self.activities = self.app.activities
        self.devices = self.app.devices
        self.assets = self.app.assets
        self.folders = self.app.folders
        self.events = self.app.events
        self.roles = self.app.roles

    def __getattr__(self, item):
        resource = self.app[item]
        self.__setattr__(item, resource)
        return self.app[item]


