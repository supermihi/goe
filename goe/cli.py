import sys
from argparse import ArgumentParser
from pprint import pprint
from typing import Type

from goe.connection import LocalHttpApiConnection
from goe.json_client import GoEJsonClient
from goe.slices.client import SliceClient


def run():
    parser = ArgumentParser('goe', add_help=False)
    parser.add_argument('-h', '--host', help='host name or IP address (local mode)')
    parser.add_argument('--help', action='store_true', help='show this help message and exit')

    sub = parser.add_subparsers(title='commands', help='available sub-commands', dest='command')

    from goe.controller import GoEControllerClient
    from goe.charger import GoEChargerClient

    add_slice_client_parser(sub, 'charger', GoEChargerClient)
    add_slice_client_parser(sub, 'controller', GoEControllerClient)

    json_parser = sub.add_parser('json')
    json_parser.add_argument('keys', nargs='*')
    json_parser.set_defaults(func=action_json)

    args = parser.parse_args()
    if args.help:
        parser.print_help()
        return
    if args.host is None:
        print('In local mode, host (-h/--host) must be given\n')
        sys.exit(1)

    args.func(args)


def action_json(args):
    connection = LocalHttpApiConnection(args.host)
    client = GoEJsonClient(connection)
    pprint(client.query(keys=args.keys))


def slice_action(args):
    client_type: Type[SliceClient] = args.client
    client = client_type.local(args.host)
    slices_by_name = {slice.NAME: slice for slice in client._SLICES}
    selected_slices = [slices_by_name[name] for name in args.slice]
    pprint(client.get_slices(*selected_slices))


def add_slice_client_parser(subparsers, name: str, client: Type[SliceClient]):
    parser = subparsers.add_parser(name, description=f'Make a query using a {client.__name__}.')
    slices = [slice.NAME for slice in client._SLICES]
    parser.add_argument('slice', metavar='SLICE', choices=slices, nargs='+',
                        help=f'Slice(s) to query. One or more of: {", ".join(slices)}')
    parser.set_defaults(func=slice_action, client=client)
