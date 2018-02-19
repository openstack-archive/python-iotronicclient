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
from iotronicclient.common.i18n import _
from iotronicclient.v1 import resource_fields as res_fields


@cliutils.arg(
    'board',
    metavar='<id>',
    help="Name or UUID of the board ")
@cliutils.arg(
    '--limit',
    metavar='<limit>',
    type=int,
    help='Maximum number of services to return per request, '
         '0 for no limit. Default is the maximum number used '
         'by the Iotronic API Service.')
@cliutils.arg(
    '--marker',
    metavar='<service>',
    help='Service UUID (for example, of the last service in the list from '
         'a previous request). Returns the list of services after this UUID.')
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
    help="Show detailed information about the services.")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more service fields. Only these fields will be fetched from "
         "the server. Can not be used when '--detail' is specified.")
def do_services_on_board(cc, args):
    """Show information about a the exposed services on a board."""
    fields = res_fields.EXPOSED_SERVICE_RESOURCE_ON_BOARD.fields
    field_labels = res_fields.EXPOSED_SERVICE_RESOURCE_ON_BOARD.labels
    list = cc.exposed_service.services_on_board(args.board)
    if list:
        cliutils.print_list(list, fields=fields,
                            field_labels=field_labels,
                            sortby_index=None,
                            json_flag=args.json)
    else:
        print(_('%s') % 'no services could be found')


@cliutils.arg('board',
              metavar='<board>',
              help="Name or UUID of the board.")
@cliutils.arg('service',
              metavar='<service>',
              help="Name or UUID of the service.")
def do_enable_service(cc, args):
    """Execute an action of the service."""

    result = cc.exposed_service.service_action(args.board,
                                               args.service,
                                               "ServiceEnable")
    print(_('%s') % result)


@cliutils.arg('board',
              metavar='<board>',
              help="Name or UUID of the board.")
@cliutils.arg('service',
              metavar='<service>',
              help="Name or UUID of the service.")
def do_disable_service(cc, args):
    """Execute an action of the service."""

    result = cc.exposed_service.service_action(args.board,
                                               args.service,
                                               "ServiceDisable")
    print(_('%s') % result)


@cliutils.arg('board',
              metavar='<board>',
              help="Name or UUID of the board.")
@cliutils.arg('service',
              metavar='<service>',
              help="Name or UUID of the service.")
def do_restore_service(cc, args):
    """Execute an action of the service."""

    result = cc.exposed_service.service_action(args.board,
                                               args.service,
                                               "ServiceRestore")
    print(_('%s') % result)


@cliutils.arg('board',
              metavar='<board>',
              help="Name or UUID of the board.")
def do_restore_services(cc, args):
    """Execute an action of the service."""

    fields = res_fields.EXPOSED_SERVICE_RESOURCE_ON_BOARD.fields
    field_labels = res_fields.EXPOSED_SERVICE_RESOURCE_ON_BOARD.labels
    list = cc.exposed_service.restore_services(args.board)
    if list:
        cliutils.print_list(list, fields=fields,
                            field_labels=field_labels,
                            sortby_index=None,
                            json_flag=args.json)
    else:
        print(_('%s') % 'no services could be found')
