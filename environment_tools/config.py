# -*- coding: utf-8 -*-
import pkgutil
import os
import yaml

def _read_data_yaml(filename):
    path = os.path.join('data', filename)
    return yaml.load(pkgutil.get_data('environment_tools', path))
