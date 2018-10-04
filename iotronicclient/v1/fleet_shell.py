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


def _print_fleet_show(fleet, fields=None, json=False):
    if fields is None:
        fields = res_fields.FLEET_DETAILED_RESOURCE.fields

    data = dict(
        [(f, getattr(fleet, f, '')) for f in fields])
    cliutils.print_dict(data, wrap=72, json_flag=json)


@cliutils.arg(
    'fleet',
    metavar='<id>',
    help="Name or UUID of the fleet ")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more fleet fields. Only these fields will be fetched from "
         "the server.")
def do_fleet_show(cc, args):
    """Show detailed information about a fleet."""
    fields = args.fields[0] if args.fields else None
    utils.check_empty_arg(args.fleet, '<id>')
    utils.check_for_invalid_fields(
        fields, res_fields.FLEET_DETAILED_RESOURCE.fields)
    fleet = cc.fleet.get(args.fleet, fields=fields)
    _print_fleet_show(fleet, fields=fields, json=args.json)


@cliutils.arg(
    '--limit',
    metavar='<limit>',
    type=int,
    help='Maximum number of fleets to return per request, '
         '0 for no limit. Default is the maximum number used '
         'by the Iotronic API Fleet.')
@cliutils.arg(
    '--marker',
    metavar='<fleet>',
    help='Fleet UUID (for example, of the last fleet in the list from '
         'a previous request). Returns the list of fleets after this UUID.')
@cliutils.arg(
    '--sort-key',
    metavar='<field>',
    help='Fleet field that will be used for sorting.')
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
    help="Show detailed information about the fleets.")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more fleet fields. Only these fields will be fetched from "
         "the server. Can not be used when '--detail' is specified.")
def do_fleet_list(cc, args):
    """List the fleets which are registered with the Iotronic fleet."""
    params = {}

    if args.detail:
        fields = res_fields.FLEET_DETAILED_RESOURCE.fields
        field_labels = res_fields.FLEET_DETAILED_RESOURCE.labels
    elif args.fields:
        utils.check_for_invalid_fields(
            args.fields[0], res_fields.FLEET_DETAILED_RESOURCE.fields)
        resource = res_fields.Resource(args.fields[0])
        fields = resource.fields
        field_labels = resource.labels
    else:
        fields = res_fields.FLEET_RESOURCE.fields
        field_labels = res_fields.FLEET_RESOURCE.labels

    sort_fields = res_fields.FLEET_DETAILED_RESOURCE.sort_fields
    sort_field_labels = res_fields.FLEET_DETAILED_RESOURCE.sort_labels

    params.update(utils.common_params_for_list(args,
                                               sort_fields,
                                               sort_field_labels))

    fleets = cc.fleet.list(**params)
    cliutils.print_list(fleets, fields,
                        field_labels=field_labels,
                        sortby_index=None,
                        json_flag=args.json)


@cliutils.arg(
    'fleet',
    metavar='<id>',
    help="Name or UUID of the fleet ")
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
def do_boards_in_fleet(cc, args):
    """List the boards which are registered in a Iotronic Fleet."""
    fields = args.fields[0] if args.fields else None
    utils.check_empty_arg(args.fleet, '<id>')
    utils.check_for_invalid_fields(
        fields, res_fields.FLEET_DETAILED_RESOURCE.fields)

    params = {}
    params['fleet'] = args.fleet

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

    boards = cc.fleet.boards_in_fleet(**params)
    cliutils.print_list(boards, fields,
                        field_labels=field_labels,
                        sortby_index=None,
                        json_flag=args.json)


@cliutils.arg(
    'name',
    metavar='<name>',
    help="Name or UUID of the fleet ")
@cliutils.arg(
    '--description',
    dest='description',
    default="",
    help="Description of the fleet")
def do_fleet_create(cc, args):
    """Register a new fleet with the Iotronic fleet."""

    field_list = ['name', 'description', 'extra']

    fields = dict((k, v) for (k, v) in vars(args).items()
                  if k in field_list and not (v is None))

    fields = utils.args_array_to_dict(fields, 'extra')

    fleet = cc.fleet.create(**fields)

    data = dict([(f, getattr(fleet, f, '')) for f in
                 res_fields.FLEET_DETAILED_RESOURCE.fields])

    cliutils.print_dict(data, wrap=72, json_flag=args.json)


@cliutils.arg('fleet',
              metavar='<fleet>',
              nargs='+',
              help="Name or UUID of the fleet.")
def do_fleet_delete(cc, args):
    """Unregister fleet(s) from the Iotronic fleet.

    Returns errors for any fleets that could not be unregistered.
    """

    failures = []
    for n in args.fleet:
        try:
            cc.fleet.delete(n)
            print(_('Deleted fleet %s') % n)
        except exceptions.ClientException as e:
            failures.append(
                _("Failed to delete fleet %(fleet)s: %(error)s")
                % {'fleet': n, 'error': e})
    if failures:
        raise exceptions.ClientException("\n".join(failures))


@cliutils.arg('fleet', metavar='<fleet>',
              help="Name or UUID of the fleet.")
@cliutils.arg(
    'attributes',
    metavar='<path=value>',
    nargs='+',
    action='append',
    default=[],
    help="Values to be changed.")
def do_fleet_update(cc, args):
    """Update information about a registered fleet."""

    patch = {k: v for k, v in (x.split('=') for x in args.attributes[0])}

    fleet = cc.fleet.update(args.fleet, patch)
    _print_fleet_show(fleet, json=args.json)
