# -*- coding: utf-8 -*-

from . import Resource


class Application(object):
    def __init__(self, organisation, application):
        self.app = Resource()[organisation][application]
        self.users = self.app['users']
        self.groups = self.app['groups']
        self.activities = self.app['activities']
        self.devices = self.app['devices']
        self.assets = self.app['assets']
        self.folders = self.app['folders']
        self.events = self.app['events']
        self.roles = self.app['roles']

    def __getattr__(self, item):
        self.__setattr__(item, self.app[item])

