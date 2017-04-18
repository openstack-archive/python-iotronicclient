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


class Plugin(base.Resource):
    def __repr__(self):
        return "<Plugin %s>" % self._info


class PluginManager(base.CreateManager):
    resource_class = Plugin
    _creation_attributes = ['name', 'code', 'public', 'callable', 'parameters',
                            'extra']
    _resource_name = 'plugins'

    def list(self, marker=None, limit=None,
             detail=False, sort_key=None, sort_dir=None, fields=None,
             public=None,
             with_public=False, all_plugins=False):
        """Retrieve a list of plugins.

        :param marker: Optional, the UUID of a plugin, eg the last
                       plugin from a previous result set. Return
                       the next result set.
        :param limit: The maximum number of results to return per
                      request, if:

            1) limit > 0, the maximum number of plugins to return.
            2) limit == 0, return the entire list of plugins.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Iotronic API
               (see Iotronic's api.max_limit option).

        :param detail: Optional, boolean whether to return detailed information
                       about plugins.

        :param sort_key: Optional, field used for sorting.

        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.

        :param fields: Optional, a list with a specified set of fields
                       of the resource to be returned. Can not be used
                       when 'detail' is set.

        :param with_public: Optional boolean value to get also public plugins.

        :param all_plugins: Optional boolean value to get all plugins.

        :returns: A list of plugins.

        """
        if limit is not None:
            limit = int(limit)

        if detail and fields:
            raise exc.InvalidAttribute(_("Can't fetch a subset of fields "
                                         "with 'detail' set"))

        filters = utils.common_filters(marker, limit, sort_key, sort_dir,
                                       fields)
        path = ''
        if not public:
            if with_public:
                filters.append('with_public=true')
            if all_plugins:
                filters.append('all_plugins=true')

            if detail:
                path += 'detail'

        else:
            path += 'public'

        if filters:
            path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path), "plugins")
        else:
            return self._list_pagination(self._path(path), "plugins",
                                         limit=limit)

    def get(self, plugin_id, fields=None):
        return self._get(resource_id=plugin_id, fields=fields)

    def delete(self, plugin_id):
        return self._delete(resource_id=plugin_id)

    def update(self, plugin_id, patch, http_method='PATCH'):
        return self._update(resource_id=plugin_id, patch=patch,
                            method=http_method)
