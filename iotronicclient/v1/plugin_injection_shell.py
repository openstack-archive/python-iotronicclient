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
from iotronicclient.v1 import resource_fields as res_fields
import json


def _print_injected(injection, fields=None, json=False):
    if fields is None:
        fields = res_fields.PLUGIN_INJECT_RESOURCE.fields

    data = dict(
        [(f, getattr(injection, f, '')) for f in fields])
    cliutils.print_dict(data, wrap=72, json_flag=json)


@cliutils.arg('board',
              metavar='<board>',
              help="Name or UUID of the board.")
@cliutils.arg('plugin',
              metavar='<plugin>',
              help="Name or UUID of the plugin.")
@cliutils.arg(
    '--onboot',
    dest='onboot',
    action='store_true',
    default=False,
    help="Start the plugin on boot")
def do_plugin_inject(cc, args):
    """Inject a plugin into a board."""
    onboot = False
    if args.onboot:
        onboot = True
    try:
        cc.plugin_injection.plugin_inject(args.board, args.plugin, onboot)
        print(_('Injected plugin %(plugin)s from board %(board)s') % {
            'board': args.board, 'plugin': args.plugin})
    except exceptions.ClientException as e:
        exceptions.ClientException(
            "Failed to inject plugin on board %(board)s: %(error)s" % {
                'board': args.board, 'error': e})


@cliutils.arg('board',
              metavar='<board>',
              help="Name or UUID of the board.")
@cliutils.arg('plugin',
              metavar='<plugin>',
              help="Name or UUID of the plugin.")
def do_plugin_remove(cc, args):
    """Remove a plugin from a board."""
    try:
        cc.plugin_injection.plugin_remove(args.board, args.plugin)
        print(_('Removed plugin %(plugin)s from board %(board)s') % {
            'board': args.board, 'plugin': args.plugin})
    except exceptions.ClientException as e:
        exceptions.ClientException(
            "Failed to remove plugin from board %(board)s: %(error)s" % {
                'board': args.board, 'error': e})


@cliutils.arg('board',
              metavar='<board>',
              help="Name or UUID of the board.")
@cliutils.arg('plugin',
              metavar='<plugin>',
              help="Name or UUID of the plugin.")
@cliutils.arg('action',
              metavar='<action>',
              help="action of the plugin.")
@cliutils.arg(
    '--params',
    metavar='<parameter=value>',
    nargs='+',
    action='append',
    default=[],
    help="Parameters of the action")
@cliutils.arg(
    '--params-file',
    metavar='<params_file>',
    help="Json file of parameters")
def do_plugin_action(cc, args):
    """Execute an action of the plugin."""
    params = {}
    if args.params_file:
        with open(args.params_file, 'r') as fil:
            params = json.load(fil)
    elif args.params:
        params = {k: v for k, v in (x.split('=') for x in args.params[0])}
    result = cc.plugin_injection.plugin_action(args.board, args.plugin,
                                               args.action, params)
    print(_('%s') % result)


@cliutils.arg(
    'board',
    metavar='<id>',
    help="Name or UUID of the board ")
def do_plugins_on_board(cc, args):
    """Show information about a the plugins injected on a board."""
    fields = res_fields.PLUGIN_INJECT_RESOURCE_ON_BOARD.fields
    field_labels = res_fields.PLUGIN_INJECT_RESOURCE_ON_BOARD.labels
    list = cc.plugin_injection.plugins_on_board(args.board)
    if list:
        cliutils.print_list(list, fields=fields,
                            field_labels=field_labels,
                            sortby_index=None,
                            json_flag=args.json)
    else:
        print(_('%s') % 'no plugin could be found')
