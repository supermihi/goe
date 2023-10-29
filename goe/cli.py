import sys
from argparse import ArgumentParser
from pprint import pprint
from typing import Type

from goe.json_client import LocalJsonClient
from goe.components.client import DeviceClientBase


def run():
    parser = ArgumentParser('goe', add_help=False)
    parser.add_argument('-h', '--host', help='host name or IP address (local mode)')
    parser.add_argument('--help', action='store_true', help='show this help message and exit')

    sub = parser.add_subparsers(title='commands', help='available sub-commands', dest='command')

    from goe.controller import GoEControllerClient
    from goe.charger import GoEChargerClient

    add_device_client_parser(sub, 'charger', GoEChargerClient)
    add_device_client_parser(sub, 'controller', GoEControllerClient)

    add_json_parser(sub)

    args = parser.parse_args()
    if args.help:
        parser.print_help()
        return
    if args.host is None:
        print('In local mode, host (-h/--host) must be given\n')
        sys.exit(1)
    if args.command is None:
        print('No subcommand given.')
        sys.exit(1)
    args.func(args)


def add_json_parser(sub):
    json_parser = sub.add_parser('json')
    json_parser.add_argument('keys', nargs='*')
    json_parser.set_defaults(func=action_json)


def action_json(args):
    client = LocalJsonClient(args.host)
    pprint(client.query(keys=args.keys))


def device_client_action(args):
    client_type: Type[DeviceClientBase] = args.client
    client = client_type.local(args.host)
    components_by_name = {component.name(): component for component in client.supported_components()}
    selected_components = [components_by_name[name] for name in args.component]
    for component in client.get_many(selected_components):
        pprint(component)


def add_device_client_parser(subparsers, name: str, client: Type[DeviceClientBase]):
    parser = subparsers.add_parser(name, description=f'Make a query using a {client.__name__}.')
    components = [component.name() for component in client.supported_components()]
    parser.add_argument('component', metavar='COMPONENT', choices=components, nargs='+',
                        help=f'Component(s) to query. One or more of: {", ".join(components)}')
    parser.set_defaults(func=device_client_action, client=client)
