# Copyright 2014 Red Hat, Inc.
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

from iotronicclient.common.i18n import _


class Resource(object):
    """Resource class

    This class is used to manage the various fields that a resource (e.g.
    Chassis, Board, Port) contains.  An individual field consists of a
    'field_id' (key) and a 'label' (value).  The caller only provides the
    'field_ids' when instantiating the object.

    Ordering of the 'field_ids' will be preserved as specified by the caller.

    It also provides the ability to exclude some of these fields when they are
    being used for sorting.
    """

    FIELDS = {
        'name': 'Name',
        'project': 'Project',
        'uuid': 'UUID',
        'extra': 'Extra',
        'updated_at': 'Updated At',
        'id': 'ID',
        'created_at': 'Created At',
        'status': 'Status',
        'code': 'Code',
        'mobile': 'Mobile',
        'session': 'Session',
        'location': 'Location',
        'owner': 'Owner',
        'type': 'Type',
        'callable': 'Callable',
        'public': 'Public',
        'onboot': 'On Boot',
        'board_uuid': 'Board',
        'plugin_uuid': 'Plugin uuid',
        'service_uuid': 'Service uuid',
        'plugin': 'Plugin',
        'parameters': 'Parameters',
        'service': 'Service',
        'port': 'Port',
        'public_port': 'Public Port',
        'pid': 'Pid',
        'protocol': 'Protocol',
        'MAC_add': 'Mac Address',
        'VIF_name': 'VIF',
        'network': 'Network',
        'ip': 'ip',
        'description': 'Description',
        'fleet': 'Fleet',
        'secure': 'Sercure',
        'http_port': 'HTTP Port',
        'https_port': 'HTTPS Port',
        'zone': 'Zone',
        'dns': 'DNS',
        'mac_addr': 'Mac Address',
        'lr_version': 'LR Version'

    }

    def __init__(self, field_ids, sort_excluded=None):
        """Create a Resource object

        :param field_ids:  A list of strings that the Resource object will
                           contain.  Each string must match an existing key in
                           FIELDS.
        :param sort_excluded: Optional. A list of strings that will not be used
                              for sorting.  Must be a subset of 'field_ids'.

        :raises: ValueError if sort_excluded contains value not in field_ids
        """
        self._fields = tuple(field_ids)
        self._labels = tuple([self.FIELDS[x] for x in field_ids])
        if sort_excluded is None:
            sort_excluded = []
        not_existing = set(sort_excluded) - set(field_ids)
        if not_existing:
            raise ValueError(
                _("sort_excluded specified with value not contained in "
                  "field_ids.  Unknown value(s): %s") % ','.join(not_existing))
        self._sort_fields = tuple(
            [x for x in field_ids if x not in sort_excluded])
        self._sort_labels = tuple([self.FIELDS[x] for x in self._sort_fields])

    @property
    def fields(self):
        return self._fields

    @property
    def labels(self):
        return self._labels

    @property
    def sort_fields(self):
        return self._sort_fields

    @property
    def sort_labels(self):
        return self._sort_labels


# Boards
BOARD_DETAILED_RESOURCE = Resource(
    [
        'uuid',
        'name',
        'type',
        'status',
        'fleet',
        'lr_version',
        'mac_addr',
        'code',
        'session',
        'mobile',
        'extra',
        'created_at',
        'updated_at',
        'location',
        'project',
        'owner',


    ],
    sort_excluded=[
        'extra', 'location', 'session',
    ])
BOARD_RESOURCE = Resource(
    ['uuid',
     'name',
     'type',
     'lr_version',
     'fleet',
     'status',
     'session',
     ])

# Plugins
PLUGIN_DETAILED_RESOURCE = Resource(
    ['uuid',
     'name',
     'owner',
     'code',
     'public',
     'callable',
     'created_at',
     'updated_at',
     'extra'

     ],
    sort_excluded=[
        'extra', 'code',
    ])
PLUGIN_RESOURCE = Resource(
    ['uuid',
     'name',
     'owner',
     'public',
     'callable',
     ])

PLUGIN_INJECT_RESOURCE_ON_BOARD = Resource(
    [
        'plugin',
        'status',
        'onboot',
        'created_at',
        'updated_at',
    ])

PLUGIN_INJECT_RESOURCE = Resource(
    ['board_uuid',
     'plugin_uuid',
     'status',
     'onboot',
     'created_at',
     'updated_at',
     ])

# Service
SERVICE_DETAILED_RESOURCE = Resource(
    ['uuid',
     'name',
     'port',
     'project',
     'protocol',
     'extra',
     'created_at',
     'updated_at',
     ],
    sort_excluded=[
        'extra',
    ])

SERVICE_RESOURCE = Resource(
    ['uuid',
     'name',
     'port',
     'protocol'
     ])

EXPOSED_SERVICE_RESOURCE_ON_BOARD = Resource(
    [
        'service',
        'public_port',
        'created_at',
        'updated_at',
    ])

EXPOSED_SERVICE_RESOURCE = Resource(
    ['board_uuid',
     'service_uuid',
     'public_port',
     'created_at',
     'updated_at',
     ])

# Port

PORT_RESOURCE = Resource(
    ['uuid',
     'MAC_add',
     'VIF_name',
     'network',
     'board_uuid',
     'ip'
     ]
)

PORT_DETAILED_RESOURCE = Resource(
    ['uuid',
     'MAC_add',
     'VIF_name',
     'network',
     'ip',
     'board_uuid',
     'extra',
     'created_at',
     'updated_at',
     ],
    sort_excluded=[
        'extra',
    ])

# Fleet

FLEET_DETAILED_RESOURCE = Resource(
    ['uuid',
     'name',
     'project',
     'description',
     'extra',
     'created_at',
     'updated_at',
     ],
    sort_excluded=[
        'extra',
    ])

FLEET_RESOURCE = Resource(
    ['uuid',
     'name',
     'project',
     'description'
     ])

# WebService
WEBSERVICE_DETAILED_RESOURCE = Resource(
    ['uuid',
     'name',
     'port',
     'secure',
     'board_uuid',
     'extra',
     'created_at',
     'updated_at',
     ],
    sort_excluded=[
        'extra',
    ])

WEBSERVICE_RESOURCE = Resource(
    ['uuid',
     'name',
     'port',
     'board_uuid',
     ])

# WebService
EXPWEBSERVICE_DETAILED_RESOURCE = Resource(
    ['board_uuid',
     'http_port',
     'https_port',
     'dns',
     'zone',
     'extra',
     'created_at',
     'updated_at',
     ],
    sort_excluded=[
        'extra',
    ])

EXPWEBSERVICE_RESOURCE = Resource(
    ['board_uuid',
     'http_port',
     'https_port',
     'dns',
     'zone',
     ])
