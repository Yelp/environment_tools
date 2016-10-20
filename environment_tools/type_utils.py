# -*- coding: utf-8 -*-
from collections import namedtuple
import os
import networkx as nx

from environment_tools.config import _read_data_json
from environment_tools.config import _convert_mapping_to_graph


# See https://github.com/Yelp/environment_tools/issues/2, for reasons that
# are unclear, creating the DiGraph on every call to this function has
# been observed to cause application memory leaks. It's probably wrong to
# do this work on every call to location_graph anyways, so let's just cache it
# This cache takes the form of a tuple(dict, DiGraph) so that if the json
# changes we can invalidate the cache immediately.
GraphCache = namedtuple('GraphCache', ('source', 'graph'))
_location_graph_cache = GraphCache(None, None)


def location_graph(use_cache=True):
    global _location_graph_cache

    location_mapping = _read_data_json('location_mapping.json')
    if not use_cache:
        return _convert_mapping_to_graph(location_mapping)

    if (_location_graph_cache.source != location_mapping):
        _location_graph_cache = GraphCache(
            source=location_mapping,
            graph=_convert_mapping_to_graph(location_mapping)
        )
    return _location_graph_cache.graph


def available_location_types():
    """ List location types supported

    :returns: list of strings that represent the hierarchy of location types
        The first type is always the most broad. The last is always the most
        specific.
    :rtype: list
    """
    return _read_data_json('location_types.json')


def compare_types(typ_1, typ_2):
    """ Compare the two provided location types

    Types are considered 'more general' if they are higher up in the hierarchy.
    For example:
        compare_types('runtimeenv', 'habitat') # runtimeenvs contain habitats
          -> negative number
        compare_types('habitat', 'ecosystem') # habitats are contained by
          -> positive number                  # ecosystems

    :returns : A negative, zero, or positive number if typ_1 is more general,
        equally general, or less general than typ_2.
    """
    i_1, i_2 = map(available_location_types().index, (typ_1, typ_2))
    return i_1 - i_2


def convert_location_type(location, source_type, desired_type):
    """ Converts the provided location into the desired location_type

    This will perform a DFS on the location graph to find connected components
    to the supplied node and then filter by the desired location_type.
    Basically if we consider our datacenter layout a DAG, then this method will
    search any nodes connected to the source location looking for the proper
    type.

    Examples:
    Assume available_location_types() is ['ecosystem', 'region', 'habitat'],
    and the location graph is:
     - prod
       - uswest1-prod
         - uswest1aprod
         - uswest1bprod

    # convert a habitat to the containing ecosystem
    convert_location_type('uswest1aprod', 'habitat', 'ecosystem') -> ['prod']
    # convert a region to the member habitats
    convert_location_type('uswest1-prod', 'region', 'habitat') ->
        ['uswest1aprod', 'uswest1bprod']

    :param location: A string that represents a location, e.g. "devc"
    :param source_type: A string that should exist inside the list returned
        by available_location_types. This is the type of the provided location
        and is optional. This exists because the names in the DAG may not be
        unique across all levels, and providing this type will disambiguate
        between which "devc" you mean (ecosystem or habitat).
    :param desired_type: A string that should exist inside the
        list returned by available_location_types. This is the desired type
        that the caller wants.
    :returns: locations, A list of locations that are of the location_type.
        These will be connected components filtered by type. Note that
        these results are sorted for calling consistency before returning.
    :rtype: list of strings
    """
    search_node = '{0}_{1}'.format(location, source_type)

    direction = compare_types(desired_type, source_type)
    candidates = set()
    if direction < 0:
        # We are converting "up", and have to walk the tree backwards
        reversed_graph = nx.reverse(location_graph())
        candidates |= set(nx.dfs_preorder_nodes(reversed_graph, search_node))
    else:
        candidates |= set(nx.dfs_preorder_nodes(location_graph(), search_node))

    # Only return results that are of the correct type
    result = filter(lambda x: x.endswith('_' + desired_type), candidates)
    return sorted([loc[:loc.rfind('_')] for loc in result])


def get_current_location(location_type):
    """ Returns the local node's location that is of the specified type

    :param location_type: A string that should exist inside the list returned
        by available_location_types. e.g. "habitat"

    :returns: location, A string that is the current node's value for the
        provided location type.
    :rtype: string
    """
    assert location_type in available_location_types()
    file_path = os.path.join('/', 'nail', 'etc', location_type)
    with open(file_path) as f:
        return f.read().strip()
