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


def _print_service_show(service, fields=None, json=False):
    if fields is None:
        fields = res_fields.SERVICE_DETAILED_RESOURCE.fields

    data = dict(
        [(f, getattr(service, f, '')) for f in fields])
    cliutils.print_dict(data, wrap=72, json_flag=json)


@cliutils.arg(
    'service',
    metavar='<id>',
    help="Name or UUID of the service ")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more service fields. Only these fields will be fetched from "
         "the server.")
def do_service_show(cc, args):
    """Show detailed information about a service."""
    fields = args.fields[0] if args.fields else None
    utils.check_empty_arg(args.service, '<id>')
    utils.check_for_invalid_fields(
        fields, res_fields.SERVICE_DETAILED_RESOURCE.fields)
    service = cc.service.get(args.service, fields=fields)
    _print_service_show(service, fields=fields, json=args.json)


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
def do_service_list(cc, args):
    """List the services which are registered with the Iotronic service."""
    params = {}

    if args.detail:
        fields = res_fields.SERVICE_DETAILED_RESOURCE.fields
        field_labels = res_fields.SERVICE_DETAILED_RESOURCE.labels
    elif args.fields:
        utils.check_for_invalid_fields(
            args.fields[0], res_fields.SERVICE_DETAILED_RESOURCE.fields)
        resource = res_fields.Resource(args.fields[0])
        fields = resource.fields
        field_labels = resource.labels
    else:
        fields = res_fields.SERVICE_RESOURCE.fields
        field_labels = res_fields.SERVICE_RESOURCE.labels

    sort_fields = res_fields.SERVICE_DETAILED_RESOURCE.sort_fields
    sort_field_labels = res_fields.SERVICE_DETAILED_RESOURCE.sort_labels

    params.update(utils.common_params_for_list(args,
                                               sort_fields,
                                               sort_field_labels))

    services = cc.service.list(**params)
    cliutils.print_list(services, fields,
                        field_labels=field_labels,
                        sortby_index=None,
                        json_flag=args.json)


@cliutils.arg(
    'name',
    metavar='<name>',
    help="Name or UUID of the service ")
@cliutils.arg(
    'port',
    metavar='<port>',
    help="Port of the service")
@cliutils.arg(
    'protocol',
    metavar='<protocol>',
    help="Protocol of the service TCP|UDP|ANY")
def do_service_create(cc, args):
    """Register a new service with the Iotronic service."""

    field_list = ['name', 'port', 'protocol', 'extra']

    fields = dict((k, v) for (k, v) in vars(args).items()
                  if k in field_list and not (v is None))

    fields = utils.args_array_to_dict(fields, 'extra')

    if fields['protocol'] not in ['TCP', 'UDP', 'ANY']:
        print("protocol must be TCP | UDP | ANY")
        return 1

    service = cc.service.create(**fields)

    data = dict([(f, getattr(service, f, '')) for f in
                 res_fields.SERVICE_DETAILED_RESOURCE.fields])

    cliutils.print_dict(data, wrap=72, json_flag=args.json)


@cliutils.arg('service',
              metavar='<service>',
              nargs='+',
              help="Name or UUID of the service.")
def do_service_delete(cc, args):
    """Unregister service(s) from the Iotronic service.

    Returns errors for any services that could not be unregistered.
    """

    failures = []
    for n in args.service:
        try:
            cc.service.delete(n)
            print(_('Deleted service %s') % n)
        except exceptions.ClientException as e:
            failures.append(
                _("Failed to delete service %(service)s: %(error)s")
                % {'service': n, 'error': e})
    if failures:
        raise exceptions.ClientException("\n".join(failures))


@cliutils.arg('service', metavar='<service>',
              help="Name or UUID of the service.")
@cliutils.arg(
    'attributes',
    metavar='<path=value>',
    nargs='+',
    action='append',
    default=[],
    help="Values to be changed.")
def do_service_update(cc, args):
    """Update information about a registered service."""

    patch = {k: v for k, v in (x.split('=') for x in args.attributes[0])}

    service = cc.service.update(args.service, patch)
    _print_service_show(service, json=args.json)
