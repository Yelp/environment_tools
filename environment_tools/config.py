# -*- coding: utf-8 -*-
import simplejson as json
import os
import pkgutil


def _read_data_json(filename):
    path = os.path.join('data', filename)
    return json.loads(pkgutil.get_data('environment_tools', path))
