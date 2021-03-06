#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This code example runs a report equal to the "Whole network report" on the
DFP website.
"""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))
import tempfile
import time

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils


def main(client):
  # Initialize appropriate services.
  report_service = client.GetService('ReportService', version='v201405')
  network_service = client.GetService('NetworkService', version='v201405')

  # Get root ad unit id for network.
  root_ad_unit_id = (
      network_service.GetCurrentNetwork()[0]['effectiveRootAdUnitId'])

  # Set filter statement and bind value for reportQuery.
  values = [{
      'key': 'parent_ad_unit_id',
      'value': {
          'xsi_type': 'NumberValue',
          'value': root_ad_unit_id
      }
  }]
  filter_statement = {'query': 'WHERE PARENT_AD_UNIT_ID = :parent_ad_unit_id',
                      'values': values}

  # Create report job.
  report_job = {
      'reportQuery': {
          'dimensions': ['DATE', 'AD_UNIT_NAME'],
          'adUnitView': 'HIERARCHICAL',
          'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                      'DYNAMIC_ALLOCATION_INVENTORY_LEVEL_IMPRESSIONS',
                      'DYNAMIC_ALLOCATION_INVENTORY_LEVEL_CLICKS',
                      'TOTAL_INVENTORY_LEVEL_IMPRESSIONS',
                      'TOTAL_INVENTORY_LEVEL_CPM_AND_CPC_REVENUE'],
          'dateRangeType': 'LAST_WEEK',
          'statement': filter_statement
      }
  }

  # Run report.
  report_job = report_service.RunReportJob(report_job)[0]

  # Wait for report to complete.
  status = report_job['reportJobStatus']
  while status != 'COMPLETED' and status != 'FAILED':
    print 'Report job with \'%s\' id is still running.' % report_job['id']
    time.sleep(30)
    status = report_service.GetReportJob(report_job['id'])[0]['reportJobStatus']

  if status == 'FAILED':
    print ('Report job with id \'%s\' failed to complete successfully.'
           % report_job['id'])
  else:
    # Change to your preferred export format.
    export_format = 'CSV_DUMP'

    report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False)

    # Download report data.
    DfpUtils.DownloadReportToFile(
        report_job['id'], export_format, report_service, report_file)

    report_file.close()

    # Display results.
    print 'Report job with id \'%s\' downloaded to:\n%s' % (
        report_job['id'], report_file.name)

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
