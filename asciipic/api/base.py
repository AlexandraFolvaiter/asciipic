# Copyright 2016 Cloudbase Solutions Srl
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

"""REST-like API base-class.

(Beginning of) the contract that all the resources must follow.
"""

import cherrypy
from oslo_log import log as logging

from asciipic import config as asciipic_config

CONFIG = asciipic_config.CONFIG
LOG = logging.getLogger(__name__)


class BaseAPI(object):

    """Contract class for all metadata providers."""

    _cp_config = {'tools.staticdir.on': False}

    exposed = True
    """Whether this application should be available for clients."""

    resources = None
    """A list that contains all the resources (endpoints) available for the
    current metadata service."""

    def __init__(self, parent=None):
        self._parent = parent
        for raw_resource in self.resources or []:
            try:
                alias, resource = raw_resource
                setattr(self, alias, resource(self))
            except ValueError:
                LOG.error("Invalid resource %r provided.", raw_resource)

    @property
    def parent(self):
        """Return the object that contains the current resource."""
        return self._parent

    # NOTE(mmicu): Desi in .pytlintrc este specificat
    # `ignored-argument-names=_.*` se pare ca nu vrea sa
    # ignore `**_kwargs`
    # pylint: disable=unused-argument
    def GET(self, **_kwargs):
        """ArestorV1 resource representation."""
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return "\n".join([endpoint for endpoint, _ in self.resources or []])


class Resource(object):

    """Contract class for all resources."""

    exposed = True
    """Whether this application should be available for clients."""

    def __init__(self, parent):
        self._parent = parent

    @property
    def parent(self):
        """Return the object that contains the current resource."""
        return self._parent
