# -*- coding: utf-8 -*-

import simplejson as json
from datetime import datetime, date, time


def jsonify_data(data):
    if data is None:
        return
    return json.dumps(data, default=json_encoder)


def json_encoder(obj):
    if isinstance(object, (datetime, date)):
        return time.mktime(obj.timetuple())
    raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

