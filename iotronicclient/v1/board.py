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


class Board(base.Resource):
    def __repr__(self):
        return "<Board %s>" % self._info


class BoardManager(base.CreateManager):
    resource_class = Board
    _creation_attributes = ['name', 'code', 'type', 'location', 'mobile',
                            'fleet', 'extra']
    _resource_name = 'boards'

    def list(self, status=None, marker=None, limit=None,
             detail=False, sort_key=None, sort_dir=None, fields=None,
             project=None):
        """Retrieve a list of boards.

        :param marker: Optional, the UUID of a board, eg the last
                       board from a previous result set. Return
                       the next result set.
        :param limit: The maximum number of results to return per
                      request, if:

            1) limit > 0, the maximum number of boards to return.
            2) limit == 0, return the entire list of boards.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Iotronic API
               (see Iotronic's api.max_limit option).

        :param detail: Optional, boolean whether to return detailed information
                       about boards.

        :param sort_key: Optional, field used for sorting.

        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.

        :param fields: Optional, a list with a specified set of fields
                       of the resource to be returned. Can not be used
                       when 'detail' is set.

        :param project: Optional string value to get
                        only boards of the project.

        :returns: A list of boards.

        """

        if limit is not None:
            limit = int(limit)

        if detail and fields:
            raise exc.InvalidAttribute(_("Can't fetch a subset of fields "
                                         "with 'detail' set"))

        filters = utils.common_filters(marker, limit, sort_key, sort_dir,
                                       fields)
        if project is not None:
            filters.append('project=%s' % project)
        if status is not None:
            filters.append('status=%s' % status)

        path = ''
        if detail:
            path += 'detail'
        if filters:
            path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path), "boards")
        else:
            return self._list_pagination(self._path(path), "boards",
                                         limit=limit)

    def get(self, board_id, fields=None):
        return self._get(resource_id=board_id, fields=fields)

    def delete(self, board_id):
        return self._delete(resource_id=board_id)

    def update(self, board_id, patch, http_method='PATCH'):
        return self._update(resource_id=board_id, patch=patch,
                            method=http_method)
