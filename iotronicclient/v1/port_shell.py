#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from iotronicclient.common import cliutils
from iotronicclient.common import utils
from iotronicclient.v1 import resource_fields as res_fields


def _print_port_show(port, fields=None, json=False):
    if fields is None:
        fields = res_fields.PORT_RESOURCE.fields

    data = dict(
        [(f, getattr(port, f, '')) for f in fields])
    cliutils.print_dict(data, wrap=72, json_flag=json)


@cliutils.arg('board',
              metavar='<board>',
              help="Name or UUID of the board.")
@cliutils.arg('port',
              metavar='<port>',
              help="Name or UUID of the port.")
def do_port_detach(cc, args):
    """Detach a port from a board."""

    cc.portonboard.detach_port(args.board, args.port)

    '''
    try:
        cc.port.attach_port(args.board, args.port)
        print(_('Port %(port)s has been detached from board %(board)s') % {
            'board': args.board, 'port': args.port})
    except exceptions.ClientException as e:
        exceptions.ClientException(
            "Failed to detach port on board %(board)s: %(error)s" % {
                'board': args.board, 'error': e})
    '''


@cliutils.arg('board',
              metavar='<board>',
              help="Name or UUID of the board.")
@cliutils.arg('network',
              metavar='<network>',
              help="Name or UUID of the network.")
@cliutils.arg('subnetwork',
              metavar='<subnetwork>',
              help="Name or UUID of the subnetwork.")
def do_port_attach(cc, args):
    """Attach a port to a board."""

    port = cc.portonboard.attach_port(args.board, args.network,
                                      args.subnetwork)
    _print_port_show(port)


@cliutils.arg(
    '--limit',
    metavar='<limit>',
    type=int,
    help='Maximum number of ports to return per request, '
         '0 for no limit. Default is the maximum number used '
         'by the Iotronic API Service.')
@cliutils.arg(
    '--marker',
    metavar='<port>',
    help='Service UUID (for example, of the last port in the list from '
         'a previous request). Returns the list of ports after this UUID.')
@cliutils.arg(
    '--sort-key',
    metavar='<field>',
    help='Service field that will be used for sorting.')
@cliutils.arg(
    '--sort-dir',
    metavar='<direction>',
    choices=['asc', 'desc'],
    help='Sort direction: "asc" (the default) or "desc".')
@cliutils.arg(
    '--detail',
    dest='detail',
    action='store_true',
    default=False,
    help="Show detailed information about the ports.")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more port fields. Only these fields will be fetched from "
         "the server. Can not be used when '--detail' is specified.")
def do_port_list(cc, args):
    """List the ports which are registered with the Iotronic port."""
    params = {}

    if args.detail:
        fields = res_fields.PORT_DETAILED_RESOURCE.fields
        field_labels = res_fields.PORT_DETAILED_RESOURCE.labels
    elif args.fields:
        utils.check_for_invalid_fields(
            args.fields[0], res_fields.PORT_DETAILED_RESOURCE.fields)
        resource = res_fields.Resource(args.fields[0])
        fields = resource.fields
        field_labels = resource.labels
    else:
        fields = res_fields.PORT_RESOURCE.fields
        field_labels = res_fields.PORT_RESOURCE.labels

    sort_fields = res_fields.PORT_DETAILED_RESOURCE.sort_fields
    sort_field_labels = res_fields.PORT_DETAILED_RESOURCE.sort_labels

    params.update(utils.common_params_for_list(args,
                                               sort_fields,
                                               sort_field_labels))

    ports = cc.port.list(**params)
    cliutils.print_list(ports, fields,
                        field_labels=field_labels,
                        sortby_index=None,
                        json_flag=args.json)
