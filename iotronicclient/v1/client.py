# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
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

from iotronicclient.common import filecache
from iotronicclient.common import http
from iotronicclient.common.http import DEFAULT_VER
from iotronicclient.common.i18n import _
from iotronicclient import exc
from iotronicclient.v1 import board
from iotronicclient.v1 import exposed_service
from iotronicclient.v1 import fleet
from iotronicclient.v1 import plugin
from iotronicclient.v1 import plugin_injection
from iotronicclient.v1 import port
from iotronicclient.v1 import service
from iotronicclient.v1 import webservice


class Client(object):
    """Client for the Iotronic v1 API.

    :param string endpoint: A user-supplied endpoint URL for the iotronic
                            service.
    :param function token: Provides token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, endpoint=None, *args, **kwargs):
        """Initialize a new client for the Iotronic v1 API."""
        if kwargs.get('os_iotronic_api_version'):
            kwargs['api_version_select_state'] = "user"
        else:
            if not endpoint:
                raise exc.EndpointException(
                    _("Must provide 'endpoint' if os_iotronic_api_version "
                      "isn't specified"))

            # If the user didn't specify a version, use a cached version if
            # one has been stored
            host, netport = http.get_server(endpoint)
            saved_version = filecache.retrieve_data(host=host, port=netport)
            if saved_version:
                kwargs['api_version_select_state'] = "cached"
                kwargs['os_iotronic_api_version'] = saved_version
            else:
                kwargs['api_version_select_state'] = "default"
                kwargs['os_iotronic_api_version'] = DEFAULT_VER

        self.http_client = http._construct_http_client(
            endpoint, *args, **kwargs)

        self.board = board.BoardManager(self.http_client)
        self.plugin = plugin.PluginManager(self.http_client)
        self.plugin_injection = plugin_injection.InjectionPluginManager(
            self.http_client)
        self.service = service.ServiceManager(self.http_client)
        self.exposed_service = exposed_service.ExposedServiceManager(
            self.http_client)
        self.port = port.PortManager(
            self.http_client)
        self.portonboard = port.PortOnBoardManager(
            self.http_client)
        self.fleet = fleet.FleetManager(self.http_client)
        self.webservice = webservice.WebServiceManager(self.http_client)
        self.webserviceonboard = webservice.WebServiceOnBoardManager(
            self.http_client)
        self.enabledwebservice = webservice.EnabledWebserviceManager(
            self.http_client)
