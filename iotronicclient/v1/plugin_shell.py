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


def _print_plugin_show(plugin, fields=None, json=False):
    if fields is None:
        fields = res_fields.PLUGIN_DETAILED_RESOURCE.fields

    data = dict(
        [(f, getattr(plugin, f, '')) for f in fields])
    cliutils.print_dict(data, wrap=72, json_flag=json)


@cliutils.arg(
    'plugin',
    metavar='<id>',
    help="Name or UUID of the plugin ")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more plugin fields. Only these fields will be fetched from "
         "the server.")
def do_plugin_show(cc, args):
    """Show detailed information about a plugin."""
    fields = args.fields[0] if args.fields else None
    utils.check_empty_arg(args.plugin, '<id>')
    utils.check_for_invalid_fields(
        fields, res_fields.PLUGIN_DETAILED_RESOURCE.fields)
    plugin = cc.plugin.get(args.plugin, fields=fields)
    _print_plugin_show(plugin, fields=fields, json=args.json)


@cliutils.arg(
    '--limit',
    metavar='<limit>',
    type=int,
    help='Maximum number of plugins to return per request, '
         '0 for no limit. Default is the maximum number used '
         'by the Iotronic API Service.')
@cliutils.arg(
    '--marker',
    metavar='<plugin>',
    help='Plugin UUID (for example, of the last plugin in the list from '
         'a previous request). Returns the list of plugins after this UUID.')
@cliutils.arg(
    '--sort-key',
    metavar='<field>',
    help='Plugin field that will be used for sorting.')
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
    help="Show detailed information about the plugins.")
@cliutils.arg(
    '--with-publics',
    dest='with_public',
    action='store_true',
    default=False,
    help="with public plugins")
@cliutils.arg(
    '--public',
    dest='public',
    action='store_true',
    default=False,
    help="get only public plugins")
@cliutils.arg(
    '--all-plugins',
    dest='all_plugins',
    action='store_true',
    default=False,
    help="all plugins")
@cliutils.arg(
    '--fields',
    nargs='+',
    dest='fields',
    metavar='<field>',
    action='append',
    default=[],
    help="One or more plugin fields. Only these fields will be fetched from "
         "the server. Can not be used when '--detail' is specified.")
def do_plugin_list(cc, args):
    """List the plugins which are registered with the Iotronic service."""
    params = {}

    if args.detail:
        fields = res_fields.PLUGIN_DETAILED_RESOURCE.fields
        field_labels = res_fields.PLUGIN_DETAILED_RESOURCE.labels
    elif args.fields:
        utils.check_for_invalid_fields(
            args.fields[0], res_fields.PLUGIN_DETAILED_RESOURCE.fields)
        resource = res_fields.Resource(args.fields[0])
        fields = resource.fields
        field_labels = resource.labels
    else:
        fields = res_fields.PLUGIN_RESOURCE.fields
        field_labels = res_fields.PLUGIN_RESOURCE.labels

    sort_fields = res_fields.PLUGIN_DETAILED_RESOURCE.sort_fields
    sort_field_labels = res_fields.PLUGIN_DETAILED_RESOURCE.sort_labels

    params.update(utils.common_params_for_list(args,
                                               sort_fields,
                                               sort_field_labels))

    if args.with_public:
        params['with_public'] = args.with_public

    if args.public:
        params['public'] = args.public

    if args.all_plugins:
        params['all_plugins'] = args.all_plugins

    plugins = cc.plugin.list(**params)
    cliutils.print_list(plugins, fields,
                        field_labels=field_labels,
                        sortby_index=None,
                        json_flag=args.json)


@cliutils.arg(
    'name',
    metavar='<name>',
    help="Name or UUID of the plugin ")
@cliutils.arg(
    'code',
    metavar='<plugin-file>',
    help="Code of the plugin")
@cliutils.arg(
    '--callable',
    dest='callable',
    action='store_true',
    default=False,
    help="Set a callable plugin")
@cliutils.arg(
    '--is-plublic',
    dest='public',
    action='store_true',
    default=False,
    help="Set a public plugin")
@cliutils.arg(
    '--params',
    metavar='<parameters>',
    help="Parameters file for the plugin")
@cliutils.arg(
    '-e', '--extra',
    metavar='<key=value>',
    action='append',
    help="Record arbitrary key/value metadata. "
         "Can be specified multiple times.")
def do_plugin_create(cc, args):
    """Register a new plugin with the Iotronic service."""

    field_list = ['name', 'code', 'callable', 'public', 'extra']

    fields = dict((k, v) for (k, v) in vars(args).items()
                  if k in field_list and not (v is None))

    fields = utils.args_array_to_dict(fields, 'extra')

    fl = fields['code']
    with open(fl, 'r') as fil:
        fields['code'] = fil.read()

    if args.params:
        fields['parameters'] = utils.json_from_file(args.params)

    plugin = cc.plugin.create(**fields)

    data = dict([(f, getattr(plugin, f, '')) for f in
                 res_fields.PLUGIN_DETAILED_RESOURCE.fields])

    cliutils.print_dict(data, wrap=72, json_flag=args.json)


@cliutils.arg('plugin',
              metavar='<plugin>',
              nargs='+',
              help="Name or UUID of the plugin.")
def do_plugin_delete(cc, args):
    """Unregister plugin(s) from the Iotronic service.

    Returns errors for any plugins that could not be unregistered.
    """

    failures = []
    for n in args.plugin:
        try:
            cc.plugin.delete(n)
            print(_('Deleted plugin %s') % n)
        except exceptions.ClientException as e:
            failures.append(_("Failed to delete plugin %(plugin)s: %(error)s")
                            % {'plugin': n, 'error': e})
    if failures:
        raise exceptions.ClientException("\n".join(failures))


@cliutils.arg('plugin', metavar='<plugin>', help="Name or UUID of the plugin.")
@cliutils.arg(
    'attributes',
    metavar='<path=value>',
    nargs='+',
    action='append',
    default=[],
    help="Values to be changed.")
def do_plugin_update(cc, args):
    """Update information about a registered plugin."""

    patch = {k: v for k, v in (x.split('=') for x in args.attributes[0])}

    plugin = cc.plugin.update(args.plugin, patch)
    _print_plugin_show(plugin, json=args.json)
