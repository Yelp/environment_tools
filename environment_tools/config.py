# -*- coding: utf-8 -*-
import json
import os

import networkx as nx

DATA_DIRECTORY = '/nail/etc/services'


def _read_data_json(filename):
    path = os.path.join(DATA_DIRECTORY, filename)
    with open(path) as f:
        return json.load(f)


def _convert_mapping_to_graph(dict_mapping):
    """ Converts the dictionary datacenter layout to a networkx.DiGraph object

    :param dict_mapping: A dict read out of the location_mapping datafile

    :returns: A :class:`networkx.DiGraph` object that is a graph representation
        of the provided mapping. Edges flow from the highest level of the
        hierarhcy to the lowest level of the hierarchy
    :rtype: :class:`networkx.DiGraph`
    """
    graph = nx.DiGraph()

    # Recursively walk the DAG, adding edges as we go
    # to the closed graph object
    def _visit(root, subdict):
        edges = [(root, key) for key in subdict]
        graph.add_edges_from(edges)
        for key, value in subdict.items():
            _visit(key, value)

    # We don't have a "root" node at the top of the DAG,
    # so this just kicks off the recursive process
    for key, value in dict_mapping.items():
        _visit(key, value)

    return graph
