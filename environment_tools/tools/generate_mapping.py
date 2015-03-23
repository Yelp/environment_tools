# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import sys
from glob import glob

import argparse
import simplejson as json

from environment_tools.type_utils import available_location_types


hierarchy = available_location_types()


def parse_options():
    parser = argparse.ArgumentParser(epilog=(
        'Deduce datacenter hierarchy based on DNS data. '
    ))
    parser.add_argument(
        'bind_directory', metavar="DIR",
        help='DNS configuration directory containing the proper zone files'
    )
    parser.add_argument(
        'destination', metavar="FILE",
        help='File name to output environment topology to'
    )
    return parser.parse_args()


def convert_locations_to_dict(locations):
    result = {}
    for sublocation in locations:
        subdict = result
        for typ in hierarchy:
            location = sublocation[typ]
            node = '{0}_{1}'.format(location, typ)
            if node not in subdict:
                subdict[node] = {}
            subdict = subdict[node]
    return result


def generate_json(args):
    source = os.path.expanduser(args.bind_directory)
    source_files = glob(os.path.join(source, 'local-*'))
    if len(source_files) == 0:
        print(
            'No bind checkout at {0}'.format(source),
            file=sys.stderr
        )
        return 1

    # Match redirection records like:
    # @  IN  DNAME  local-devc.yelpcorp.com.
    dname_regex = '^\s*@\s+IN\s+DNAME\s+'

    # Match TXT records like:
    # habitat  IN  TXT  devc
    txt_regex = '(\S+)\s+IN\s+TXT\s+(\S+)'

    locations = []
    for bind_file in source_files:
        with open(bind_file) as bind_data_file:
            bind_data = bind_data_file.read()
            # First check that we don't have a DNS redirect, in which
            # case the TXT records in this bind file are either not actually
            # useful, may be contradictory, or incomplete
            if re.search(dname_regex, bind_data, re.MULTILINE) is None:
                # If we are in a proper local zone, read all the TXT records
                # present in the bind file and store the key -> value lookups
                # Generates matches like:
                # [('habitat', 'sfo2'), ('superregion', 'norcal-prod'), ...]
                matches = re.findall(txt_regex, bind_data, re.MULTILINE)
                txt_dictionary = dict(matches)
                # We require a txt record for each part of our datacenter
                # machine hierarchy
                location = dict([(k, txt_dictionary[k]) for k in hierarchy])
                locations.append(location)

    dict_representation = convert_locations_to_dict(locations)
    with open(args.destination, 'w') as f:
        json.dump(dict_representation, f, indent=2, sort_keys=True)

    return 0


def main():
    args = parse_options()
    sys.exit(generate_json(args))


if __name__ == '__main__':
    main()
