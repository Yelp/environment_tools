# -*- coding: utf-8 -*-
import os

from environment_tools.config import _read_data_json


location_mapping = _read_data_json('location_mapping.json')
location_types = _read_data_json('location_types.json')


def available_location_types():
    """ Location types Yelp supports

    :returns: list of strings that represent the hierarchy of location types
        at Yelp. The first type is always the most broad. The last is always
        the most specific.
    :rtype: list
    """
    return location_types


def convert_location_type(location, location_type):
    """ Converts the provided location into the desired location_type

    This will perform a search on the Yelp datacenter graph to find connected
    components to the supplied node and then filter by the desired
    location_type. Basically if we consider our datacenter layout a DAG, then
    this method will search any nodes connected to the source location looking
    for the proper type.

    Examples:
    # convert a habitat to the containing ecosystem
    convert_location_type('sfo1', 'ecosystem') -> ['prod']
    # convert a region to the member habitats
    convert_location_type('sfo12', 'habitat') -> ['sfo1', 'sfo2']

    :param location: A string that represents a yelp location, e.g. "devc"
    :param location_type: A string that should exist inside the
        list returned by available_location_types. This is the desired type
        that the caller wants.

    :returns: locations, A list of locations that are of the location_type.
        These will be connected components filtered by type.
    :rtype: list of strings
    """
    assert location_type in available_location_types()
    return ["noop"]


def get_current_location(location_type):
    """ Returns the current node's location that is of the specified type

    :param location_type: A string that should exist inside the list returned
        by available_location_types. e.g. "habitat"

    :returns: location, A string that is the current node's value for the
        provided location type.
    :rtype: string
    """
    assert location_type in location_types
    file_path = os.path.join('/', 'nail', 'etc', location_type)
    with open(file_path) as f:
        return f.read().strip()
