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


def _print_webservice_enabled_show(expwebservice, fields=None, json=False):
    print(expwebservice)

    if fields is None:
        fields = res_fields.EXPWEBSERVICE_DETAILED_RESOURCE.fields

    data = dict(
        [(f, getattr(expwebservice, f, '')) for f in fields])
    cliutils.print_dict(data, wrap=72, json_flag=json)


def _print_webservice_show(webservice, fields=None, json=False):
    if fields is None:
        fields = res_fields.WEBSERVICE_DETAILED_RESOURCE.fields

    data = dict(
        [(f, getattr(webservice, f, '')) for f in fields])
    cliutils.print_dict(data, wrap=72, json_flag=json)


@cliutils.arg(
    'webservice',
    metavar='<id>',
    help="Name or UUID of the webservice ")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more webservice fields. Only these fields will be fetched "
         "from the server.")
def do_webservice_show(cc, args):
    """Show detailed information about a webservice."""
    fields = args.fields[0] if args.fields else None
    utils.check_empty_arg(args.webservice, '<id>')
    utils.check_for_invalid_fields(
        fields, res_fields.WEBSERVICE_DETAILED_RESOURCE.fields)
    webservice = cc.webservice.get(args.webservice, fields=fields)
    _print_webservice_show(webservice, fields=fields, json=args.json)


@cliutils.arg(
    '--limit',
    metavar='<limit>',
    type=int,
    help='Maximum number of webservices to return per request, '
         '0 for no limit. Default is the maximum number used '
         'by the Iotronic API WebService.')
@cliutils.arg(
    '--marker',
    metavar='<webservice>',
    help='WebService UUID (for example, of the last webservice in the list '
         'from a previous request). '
         'Returns the list of webservices after this UUID.')
@cliutils.arg(
    '--sort-key',
    metavar='<field>',
    help='WebService field that will be used for sorting.')
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
    help="Show detailed information about the webservices.")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more webservice fields. Only these fields will be fetched "
         "from the server. Can not be used when '--detail' is specified.")
def do_webservice_list(cc, args):
    """List the webservices which are registered with the
    Iotronic webservice.

    """
    params = {}

    if args.detail:
        fields = res_fields.WEBSERVICE_DETAILED_RESOURCE.fields
        field_labels = res_fields.WEBSERVICE_DETAILED_RESOURCE.labels
    elif args.fields:
        utils.check_for_invalid_fields(
            args.fields[0], res_fields.WEBSERVICE_DETAILED_RESOURCE.fields)
        resource = res_fields.Resource(args.fields[0])
        fields = resource.fields
        field_labels = resource.labels
    else:
        fields = res_fields.WEBSERVICE_RESOURCE.fields
        field_labels = res_fields.WEBSERVICE_RESOURCE.labels

    sort_fields = res_fields.WEBSERVICE_DETAILED_RESOURCE.sort_fields
    sort_field_labels = res_fields.WEBSERVICE_DETAILED_RESOURCE.sort_labels

    params.update(utils.common_params_for_list(args,
                                               sort_fields,
                                               sort_field_labels))

    webservices = cc.webservice.list(**params)
    cliutils.print_list(webservices, fields,
                        field_labels=field_labels,
                        sortby_index=None,
                        json_flag=args.json)


@cliutils.arg(
    'board',
    metavar='<board>',
    help="Name or UUID of the board ")
@cliutils.arg(
    'name',
    metavar='<name>',
    help="Name of the webservice ")
@cliutils.arg(
    'port',
    metavar='<port>',
    help="Port of the webservice")
@cliutils.arg(
    '--secure',
    dest='secure',
    action='store_true',
    default=True,
    help="Set a secure webservice")
def do_expose_webservice(cc, args):
    """Register a new webservice with the Iotronic webservice."""

    webservice = cc.webserviceonboard.expose(args.board,
                                             args.name,
                                             args.port,
                                             args.secure)

    data = dict([(f, getattr(webservice, f, '')) for f in
                 res_fields.WEBSERVICE_DETAILED_RESOURCE.fields])

    cliutils.print_dict(data, wrap=72, json_flag=args.json)


#

@cliutils.arg('webservice',
              metavar='<webservice>',
              nargs='+',
              help="Name or UUID of the webservice.")
def do_unexpose_webservice(cc, args):
    """Unregister webservice(s) from the Iotronic webservice.

    Returns errors for any webservices that could not be unregistered.
    """

    failures = []
    for n in args.webservice:
        try:
            cc.webservice.delete(n)
            print(_('Deleted webservice %s') % n)
        except exceptions.ClientException as e:
            failures.append(
                _("Failed to delete webservice %(webservice)s: %(error)s")
                % {'webservice': n, 'error': e})
    if failures:
        raise exceptions.ClientException("\n".join(failures))


# @cliutils.arg('webservice', metavar='<webservice>',
#               help="Name or UUID of the webservice.")
# @cliutils.arg(
#     'attributes',
#     metavar='<path=value>',
#     nargs='+',
#     action='append',
#     default=[],
#     help="Values to be changed.")
# def do_webservice_update(cc, args):
#     """Update information about a registered webservice."""
#
#     patch = {k: v for k, v in (x.split('=') for x in args.attributes[0])}
#
#     webservice = cc.webservice.update(args.webservice, patch)
#     _print_webservice_show(webservice, json=args.json)

@cliutils.arg(
    'board',
    metavar='<board_uuid>',
    help="UUID or name of the board ")
@cliutils.arg(
    '--limit',
    metavar='<limit>',
    type=int,
    help='Maximum number of webservices to return per request, '
         '0 for no limit. Default is the maximum number used '
         'by the Iotronic API WebService.')
@cliutils.arg(
    '--marker',
    metavar='<webservice>',
    help='WebService UUID (for example, of the last webservice in the list '
         'from a previous request). Returns the list of webservices '
         'after this UUID.')
@cliutils.arg(
    '--sort-key',
    metavar='<field>',
    help='WebService field that will be used for sorting.')
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
    help="Show detailed information about the webservices.")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more webservice fields. Only these fields will be fetched "
         "from the server. Can not be used when '--detail' is specified.")
def do_webservices_on_board(cc, args):
    """List the webservices which are registered
    with the Iotronic webservice.

    """
    params = {}

    if args.detail:
        fields = res_fields.WEBSERVICE_DETAILED_RESOURCE.fields
        field_labels = res_fields.WEBSERVICE_DETAILED_RESOURCE.labels
    elif args.fields:
        utils.check_for_invalid_fields(
            args.fields[0], res_fields.WEBSERVICE_DETAILED_RESOURCE.fields)
        resource = res_fields.Resource(args.fields[0])
        fields = resource.fields
        field_labels = resource.labels
    else:
        fields = res_fields.WEBSERVICE_RESOURCE.fields
        field_labels = res_fields.WEBSERVICE_RESOURCE.labels

    sort_fields = res_fields.WEBSERVICE_DETAILED_RESOURCE.sort_fields
    sort_field_labels = res_fields.WEBSERVICE_DETAILED_RESOURCE.sort_labels

    params.update(utils.common_params_for_list(args,
                                               sort_fields,
                                               sort_field_labels))

    webservices = cc.webserviceonboard.list(args.board, **params)
    cliutils.print_list(webservices, fields,
                        field_labels=field_labels,
                        sortby_index=None,
                        json_flag=args.json)


@cliutils.arg(
    'board',
    metavar='<board_uuid>',
    help="UUID or name of the board ")
@cliutils.arg(
    'dns',
    metavar='<dns>',
    help="UUID of the webservice ")
@cliutils.arg(
    'zone',
    metavar='<zone>',
    help="UUID of the board ")
@cliutils.arg(
    'email',
    metavar='<email>',
    help="UUID of the webservice ")
def do_enable_webservices(cc, args):
    webservices = cc.webserviceonboard.enable_webservice(args.board,
                                                         args.dns,
                                                         args.zone,
                                                         args.email)
    _print_webservice_enabled_show(webservices, json=args.json)


@cliutils.arg(
    'board',
    metavar='<board_uuid>',
    help="UUID of the board ")
def do_disable_webservices(cc, args):
    cc.webserviceonboard.disable_webservice(args.board)


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
def do_enabled_webservice_list(cc, args):
    """List the services which are registered with the Iotronic service."""
    params = {}

    if args.detail:
        fields = res_fields.EXPWEBSERVICE_DETAILED_RESOURCE.fields
        field_labels = res_fields.EXPWEBSERVICE_DETAILED_RESOURCE.labels
    elif args.fields:
        utils.check_for_invalid_fields(
            args.fields[0], res_fields.EXPWEBSERVICE_DETAILED_RESOURCE.fields)
        resource = res_fields.Resource(args.fields[0])
        fields = resource.fields
        field_labels = resource.labels
    else:
        fields = res_fields.EXPWEBSERVICE_RESOURCE.fields
        field_labels = res_fields.EXPWEBSERVICE_RESOURCE.labels

    sort_fields = res_fields.EXPWEBSERVICE_DETAILED_RESOURCE.sort_fields
    sort_field_labels = res_fields.EXPWEBSERVICE_DETAILED_RESOURCE.sort_labels

    params.update(utils.common_params_for_list(args,
                                               sort_fields,
                                               sort_field_labels))

    enabWebservices = cc.enabledwebservice.list(**params)
    cliutils.print_list(enabWebservices, fields,
                        field_labels=field_labels,
                        sortby_index=None,
                        json_flag=args.json)
