# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright 2012 Nebula, Inc.
# Copyright 2013 IBM Corp.
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

import datetime
import urllib

from nova.openstack.common import timeutils
from nova.tests.integrated.v3 import test_servers


class SimpleTenantUsageSampleJsonTest(test_servers.ServersSampleBase):
    extension_name = "os-simple-tenant-usage"
    section_name = 'Simple Tenant Usage'
    section_doc = "Provide simple tenant usage for tenant."

    def setUp(self):
        """setUp method for simple tenant usage."""
        super(SimpleTenantUsageSampleJsonTest, self).setUp()

        self.started = timeutils.utcnow()
        self.now = self.started + datetime.timedelta(hours=1)

        timeutils.set_time_override(self.started)
        self._post_server()
        timeutils.set_time_override(self.now)

    def tearDown(self):
        """tearDown method for simple tenant usage."""
        super(SimpleTenantUsageSampleJsonTest, self).tearDown()
        timeutils.clear_time_override()

    def test_get_tenants_usage(self):
        # Get api sample to get all tenants usage request.
        response = self._doc_do_get(
            'os-simple-tenant-usage?start=%s&end=%s',
            (urllib.quote(str(self.started)), urllib.quote(str(self.now))),
            ('period_start', 'period_stop'),
            api_desc="Retrieve tenant_usage for all tenants.")
        subs = self._get_regexes()
        self._verify_response('simple-tenant-usage-get', subs, response, 200)

    def test_get_tenant_usage_details(self):
        # Get api sample to get specific tenant usage request.
        tenant_id = 'openstack'
        response = self._doc_do_get(
            'os-simple-tenant-usage/%s?start=%s&end=%s',
            (tenant_id, urllib.quote(str(self.started)),
             urllib.quote(str(self.now))),
            ('tenant_id', 'period_start', 'period_stop'),
            api_desc="Retrieve tenant_usage for a specified tenant.")
        subs = self._get_regexes()
        self._verify_response('simple-tenant-usage-get-specific', subs,
                              response, 200)


class SimpleTenantUsageSampleXmlTest(SimpleTenantUsageSampleJsonTest):
    ctype = "xml"
