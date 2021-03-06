#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
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

"""This example gets all campaigns with a specific label.

To add a label to campaigns, run add_campaign_labels.py.

The AdWordsClient is pulling credentials and properties from a
"adwords_api_auth.pkl" file. By default, it looks for this file in your home
directory.

Tags: CampaignService.get
"""

__author__ = 'Mark Saniscalchi'

import os
import sys
import time
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

from adspygoogle import AdWordsClient


LABEL_ID = 'INSERT_LABEL_ID_HERE'
PAGE_SIZE = 100


def main(client, label_id):
  # Initialize appropriate service.
  campaign_service = client.GetCampaignService(version='v201406')

  offset = 0
  selector = {
      'fields': ['Id', 'Name', 'Labels'],
      # Labels filtering is performed by ID. You can use CONTAINS_ANY to select
      # campaigns with any of the label IDs, CONTAINS_ALL to select campaigns
      # with all of the label IDs, or CONTAINS_NONE to select campaigns with
      # none of the label IDs.
      'ordering': [{
          'field': 'Name',
          'sortOrder': 'ASCENDING'
          }],
      'paging': {
          'startIndex': str(offset),
          'numberResults': str(PAGE_SIZE)
      },
      'predicates': [{
          'field': 'Labels',
          'operator': 'CONTAINS_ANY',
          'values': [label_id]
      }]
  }

  more_pages = True
  while more_pages:
    page = campaign_service.Get(selector)[0]

    # Display results.
    if 'entries' in page:
      for campaign in page['entries']:
        print ('Campaign found with Id \'%s\', name \'%s\', and labels: %s'
               % (campaign['id'], campaign['name'], campaign['labels']))
    else:
      print 'No campaigns were found.'

    offset += PAGE_SIZE
    selector['paging']['startIndex'] = str(offset)
    more_pages = offset < int(page['totalNumEntries'])
    time.sleep(1)


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, LABEL_ID)
