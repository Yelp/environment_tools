# -*- coding: utf-8 -*-
import re

from environment_tools import type_utils

NODE_NAME_FORMAT = '[A-Za-z0-9]*(-[A-Za-z0-9]*)*-(?P<location>[A-Za-z0-9]*)($|\..*)'


def get_node_location(node, name_format=NODE_NAME_FORMAT):
    """ Parses the node location from the provided node hostname.

    :param node: A string that reprsents the node's hostname eg "my-machine-devb.place.com"
    :param name_format: A string that represents the regex to parse the node's location from
        the full hostname. Must have the capture group 'location' defined to correctly parse
        the location.
    :returns: node_location, The location of the given hostname or None if not found.
    :rtype: String or None
    """
    matches = re.search(name_format, node)
    if not matches:
        return None
    else:
        node_location = matches.group('location')
        return node_location


def get_node_location_type(node_location):
    """ Given a node location returns the location_type of that node.

    For example:
       Assume type_utils.available_location_types() is ['ecosystem', 'region', 'habitat'],
       and the location graph is:
        - prod
          - uswest1-prod
            - uswest1aprod
            - uswest1bprod

        get_node_location('uswest1aprod') -> 'habitat'
        get_node_location('uswest1-prod') -> 'region'

    :param node_location: A string that represents a node's location
    :returns: location_type, The location type that corresponds to that node's location.
    :rtype: String
    """
    location_graph = type_utils.location_graph()
    for location_type in type_utils.available_location_types():
        if location_graph.has_node('{}_{}'.format(node_location, location_type)):
            return location_type
    raise ValueError('{} not found in environment'.format(node_location))


def node_location_equality(node_1, node_2, location_type):
    """ Checks if two nodes are equal for a specific location type.

    For example:
       Assume type_utils.available_location_types() is ['ecosystem', 'region', 'habitat'],
       and the location graph is:
        - prod
          - uswest1-prod
            - uswest1aprod
            - uswest1bprod

        node_location_equality('uswest1aprod', uswest1bprod', 'habitat') -> False
        node_location_equality('uswest1aprod', uswest1bprod', 'region') -> True

    :param node_1: A string that represents a node
    :param node_2: A string that represents a node
    :param location_type: A string that represents the location_type to use to compare the
        two nodes.
    :returns: True or False.
    :rtype: bool
    """
    node_1_location_type = get_node_location_type(node_1)
    if node_1_location_type != location_type:
        node_1 = type_utils.convert_location_type(node_1, node_1_location_type, location_type)
    node_2_location_type = get_node_location_type(node_2)
    if node_2_location_type != location_type:
        node_2 = type_utils.convert_location_type(node_2, node_2_location_type, location_type)
    return node_1 == node_2
