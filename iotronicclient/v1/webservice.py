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

import logging

from iotronicclient.common import base
from iotronicclient.common.i18n import _
from iotronicclient.common import utils
from iotronicclient import exc

LOG = logging.getLogger(__name__)
_DEFAULT_POLL_INTERVAL = 2


class WebService(base.Resource):
    def __repr__(self):
        return "<WebService %s>" % self._info


class WebServiceManager(base.CreateManager):
    resource_class = WebService
    _creation_attributes = ['name', 'port', 'protocol', 'secure', 'extra']

    _resource_name = 'webservices'

    def list(self, marker=None, limit=None,
             detail=False, sort_key=None, sort_dir=None, fields=None):
        """Retrieve a list of webservices.

        :param marker: Optional, the UUID of a webservice, eg the last
                       webservice from a previous result set. Return
                       the next result set.
        :param limit: The maximum number of results to return per
                      request, if:

            1) limit > 0, the maximum number of webservices to return.
            2) limit == 0, return the entire list of webservices.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Iotronic API
               (see Iotronic's api.max_limit option).

        :param detail: Optional, boolean whether to return detailed information
                       about webservices.

        :param sort_key: Optional, field used for sorting.

        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.

        :param fields: Optional, a list with a specified set of fields
                       of the resource to be returned. Can not be used
                       when 'detail' is set.

        :returns: A list of webservices.

        """
        if limit is not None:
            limit = int(limit)

        if detail and fields:
            raise exc.InvalidAttribute(_("Can't fetch a subset of fields "
                                         "with 'detail' set"))

        filters = utils.common_filters(marker, limit, sort_key, sort_dir,
                                       fields)
        path = ''

        if detail:
            path += 'detail'

        if filters:
            path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path), "webservices")
        else:
            return self._list_pagination(self._path(path), "webservices",
                                         limit=limit)

    def get(self, webservice_id, fields=None):
        return self._get(resource_id=webservice_id, fields=fields)

    def delete(self, webservice_id):
        return self._delete(resource_id=webservice_id)
    #
    # def update(self, webservice_id, patch, http_method='PATCH'):
    #     return self._update(resource_id=webservice_id, patch=patch,
    #                         method=http_method)


class WebServiceOnBoardManager(base.CreateManager):
    resource_class = WebService
    _creation_attributes = ['name', 'port', 'protocol', 'extra']

    _resource_name = 'boards'

    def list(self, board_ident, marker=None, limit=None,
             detail=False, sort_key=None, sort_dir=None, fields=None):
        """Retrieve a list of webservices on a board.

        :param marker: Optional, the UUID of a webservice, eg the last
                       webservice from a previous result set. Return
                       the next result set.
        :param limit: The maximum number of results to return per
                      request, if:

            1) limit > 0, the maximum number of webservices to return.
            2) limit == 0, return the entire list of webservices.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Iotronic API
               (see Iotronic's api.max_limit option).

        :param detail: Optional, boolean whether to return detailed information
                       about webservices.

        :param sort_key: Optional, field used for sorting.

        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.

        :param fields: Optional, a list with a specified set of fields
                       of the resource to be returned. Can not be used
                       when 'detail' is set.

        :returns: A list of webservices.

        """
        if limit is not None:
            limit = int(limit)

        if detail and fields:
            raise exc.InvalidAttribute(_("Can't fetch a subset of fields "
                                         "with 'detail' set"))

        filters = utils.common_filters(marker, limit, sort_key, sort_dir,
                                       fields)

        path = "%s/webservices" % board_ident

        if detail:
            path += 'detail'

        if filters:
            path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path), "webservices")
        else:
            return self._list_pagination(self._path(path), "webservices",
                                         limit=limit)

    def expose(self, board_ident, name, port, secure):
        path = "%s/webservices" % board_ident

        body = {
            "name": name,
            "port": port,
            "secure": secure
        }
        resp, body = self.api.json_request('PUT', self._path(path), body=body)
        return WebService(self, body)

    def enable_webservice(self, board_ident, dns, zone, email,
                          http_method='POST'):
        path = "%s/webservices/enable" % board_ident

        body = {
            "dns": dns,
            "zone": zone,
            "email": email
        }
        resp, body = self.api.json_request(http_method, self._path(path),
                                           body=body)
        return EnabledWebservice(self, body)

    def disable_webservice(self, board_ident):
        path = "%s/webservices/disable" % board_ident

        return self.api.raw_request('DELETE', self._path(path))


class EnabledWebservice(base.Resource):
    def __repr__(self):
        return "<EnabledWebservice %s>" % self._info


class EnabledWebserviceManager(base.CreateManager):
    resource_class = EnabledWebservice
    _creation_attributes = ['board_uuid', 'https_port', 'http_port', 'dns',
                            'zone', 'extra']

    _resource_name = 'enabledwebservices'

    def list(self, marker=None, limit=None,
             detail=False, sort_key=None, sort_dir=None, fields=None):
        """Retrieve a list of enabledenabledwebservices on a board.

        :param marker: Optional, the UUID of a enabledwebservice, eg the last
                       enabledwebservice from a previous result set. Return
                       the next result set.
        :param limit: The maximum number of results to return per
                      request, if:

            1) limit > 0, the maximum number of enabledwebservices to return.
            2) limit == 0, return the entire list of enabledwebservices.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Iotronic API
               (see Iotronic's api.max_limit option).

        :param detail: Optional, boolean whether to return detailed information
                       about enabledwebservices.

        :param sort_key: Optional, field used for sorting.

        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.

        :param fields: Optional, a list with a specified set of fields
                       of the resource to be returned. Can not be used
                       when 'detail' is set.

        :returns: A list of enabledwebservices.

        """
        if limit is not None:
            limit = int(limit)

        if detail and fields:
            raise exc.InvalidAttribute(_("Can't fetch a subset of fields "
                                         "with 'detail' set"))

        filters = utils.common_filters(marker, limit, sort_key, sort_dir,
                                       fields)
        path = ''

        if detail:
            path += 'detail'

        if filters:
            path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path), "EnabledWebservices")
        else:
            return self._list_pagination(self._path(path),
                                         "EnabledWebservices",
                                         limit=limit)
