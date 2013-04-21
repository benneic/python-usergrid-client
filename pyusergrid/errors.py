# -*- coding: utf-8 -*-


class UsergridError(Exception):
    pass


class UsergridResponseError(UsergridError):
    def __init__(self, response):
        self.error = response.error
        self.error_description = response.error_description
        self.response = response

