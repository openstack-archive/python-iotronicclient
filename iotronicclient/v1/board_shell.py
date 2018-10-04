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

from iotronicclient.common.apiclient import exceptions
from iotronicclient.common import cliutils
from iotronicclient.common.i18n import _
from iotronicclient.common import utils
from iotronicclient.v1 import resource_fields as res_fields


def _print_board_show(board, fields=None, json=False):
    if fields is None:
        fields = res_fields.BOARD_DETAILED_RESOURCE.fields

    data = dict(
        [(f, getattr(board, f, '')) for f in fields])
    cliutils.print_dict(data, wrap=72, json_flag=json)


@cliutils.arg(
    'board',
    metavar='<id>',
    help="Name or UUID of the board ")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more board fields. Only these fields will be fetched from "
         "the server.")
def do_board_show(cc, args):
    """Show detailed information about a board."""
    fields = args.fields[0] if args.fields else None
    utils.check_empty_arg(args.board, '<id>')
    utils.check_for_invalid_fields(
        fields, res_fields.BOARD_DETAILED_RESOURCE.fields)
    board = cc.board.get(args.board, fields=fields)
    _print_board_show(board, fields=fields, json=args.json)


@cliutils.arg(
    '--limit',
    metavar='<limit>',
    type=int,
    help='Maximum number of boards to return per request, '
         '0 for no limit. Default is the maximum number used '
         'by the Iotronic API Service.')
@cliutils.arg(
    '--marker',
    metavar='<board>',
    help='Board UUID (for example, of the last board in the list from '
         'a previous request). Returns the list of boards after this UUID.')
@cliutils.arg(
    '--sort-key',
    metavar='<field>',
    help='Board field that will be used for sorting.')
@cliutils.arg(
    '--status',
    metavar='<field>',
    help='Filter by board status ')
@cliutils.arg(
    '--sort-dir',
    metavar='<direction>',
    choices=['asc', 'desc'],
    help='Sort direction: "asc" (the default) or "desc".')
@cliutils.arg(
    '--project',
    metavar='<project>',
    help="Project of the list.")
@cliutils.arg(
    '--detail',
    dest='detail',
    action='store_true',
    default=False,
    help="Show detailed information about the boards.")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more board fields. Only these fields will be fetched from "
         "the server. Can not be used when '--detail' is specified.")
def do_board_list(cc, args):
    """List the boards which are registered with the Iotronic service."""
    params = {}

    if args.status:
        params['status'] = args.status

    if args.project is not None:
        params['project'] = args.project

    if args.detail:
        fields = res_fields.BOARD_DETAILED_RESOURCE.fields
        field_labels = res_fields.BOARD_DETAILED_RESOURCE.labels
    elif args.fields:
        utils.check_for_invalid_fields(
            args.fields[0], res_fields.BOARD_DETAILED_RESOURCE.fields)
        resource = res_fields.Resource(args.fields[0])
        fields = resource.fields
        field_labels = resource.labels
    else:
        fields = res_fields.BOARD_RESOURCE.fields
        field_labels = res_fields.BOARD_RESOURCE.labels

    sort_fields = res_fields.BOARD_DETAILED_RESOURCE.sort_fields
    sort_field_labels = res_fields.BOARD_DETAILED_RESOURCE.sort_labels

    params.update(utils.common_params_for_list(args,
                                               sort_fields,
                                               sort_field_labels))

    boards = cc.board.list(**params)
    cliutils.print_list(boards, fields,
                        field_labels=field_labels,
                        sortby_index=None,
                        json_flag=args.json)


@cliutils.arg(
    'name',
    metavar='<name>',
    help="Name or UUID of the board ")
@cliutils.arg(
    'code',
    metavar='<code>',
    help="Codeof the board ")
@cliutils.arg(
    'type',
    metavar='<type>',
    help="Type of the board ")
@cliutils.arg(
    'latitude',
    metavar='<latitude>',
    help="Latitude of the board ")
@cliutils.arg(
    'longitude',
    metavar='<longitude>',
    help="Longitude of the board ")
@cliutils.arg(
    'altitude',
    metavar='<altitude>',
    help="Altitude of the board ")
@cliutils.arg(
    '--fleet',
    metavar='<fleet>',
    help="Fleet of the board.")
@cliutils.arg(
    '--mobile',
    dest='mobile',
    action='store_true',
    default=False,
    help="Set a mobile board")
@cliutils.arg(
    '-e', '--extra',
    metavar='<key=value>',
    action='append',
    help="Record arbitrary key/value metadata. "
         "Can be specified multiple times.")
def do_board_create(cc, args):
    """Register a new board with the Iotronic service."""
    field_list = ['name', 'code', 'type', 'mobile', 'fleet', 'extra']

    fields = dict((k, v) for (k, v) in vars(args).items()
                  if k in field_list and not (v is None))
    fields = utils.args_array_to_dict(fields, 'extra')

    fields['location'] = [
        {'latitude': args.latitude, 'longitude': args.longitude,
         'altitude': args.altitude}]

    board = cc.board.create(**fields)
    data = dict([(f, getattr(board, f, '')) for f in
                 res_fields.BOARD_DETAILED_RESOURCE.fields])
    cliutils.print_dict(data, wrap=72, json_flag=args.json)


@cliutils.arg('board',
              metavar='<board>',
              nargs='+',
              help="Name or UUID of the board.")
def do_board_delete(cc, args):
    """Unregister board(s) from the Iotronic service.

    Returns errors for any boards that could not be unregistered.
    """

    failures = []
    for n in args.board:
        try:
            cc.board.delete(n)
            print(_('Deleted board %s') % n)
        except exceptions.ClientException as e:
            failures.append(_("Failed to delete board %(board)s: %(error)s")
                            % {'board': n, 'error': e})
    if failures:
        raise exceptions.ClientException("\n".join(failures))


@cliutils.arg('board', metavar='<board>', help="Name or UUID of the board.")
@cliutils.arg(
    'attributes',
    metavar='<path=value>',
    nargs='+',
    action='append',
    default=[],
    help="Values to be changed.")
def do_board_update(cc, args):
    """Update information about a registered board."""

    patch = {k: v for k, v in (x.split('=') for x in args.attributes[0])}

    board = cc.board.update(args.board, patch)
    _print_board_show(board, json=args.json)
