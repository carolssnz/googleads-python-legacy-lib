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

"""This code example deletes content metadata key hierarchies.

To determine which content metadata key hierarchies exist, run
get_all_content_metadata_key_hierarchies.py.

This feature is only available to DFP video publishers.

Tags: ContentMetadataKeyHierarchyService.getContentMetadataKeyHierarchiesByStatement
      ContentMetadataKeyHierarchyService.perfomContentMetadataKeyHierarchyAction
"""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils

# Set the ID of the content metadata key hierarchy to delete.
CONTENT_METADATA_KEY_HIERARCHY_ID = (
    'INSERT_CONTENT_METADATA_KEY_HIERARCHY_ID_HERE')


def main(client, content_metadata_key_hierarchy_id):
  # Initialize appropriate service.
  content_metadata_key_hierarchy_service = client.GetService(
      'ContentMetadataKeyHierarchyService', version='v201408')

  # Create a query to select a single content metadata key hierarchy.
  values = [{
      'key': 'id',
      'value': {
          'xsi_type': 'NumberValue',
          'value': content_metadata_key_hierarchy_id
      }
  }]

  query = 'WHERE id = :id ORDER BY id ASC'
  statement = DfpUtils.FilterStatement(query, values, 1)

  # Get a single content metadata key hierarchy by statement.
  response = (content_metadata_key_hierarchy_service
              .GetContentMetadataKeyHierarchiesByStatement(
                  statement.ToStatement())[0])
  content_metadata_key_hierarchies = response.get('results')

  # Display results.
  if content_metadata_key_hierarchies:
    for content_metadata_key_hierarchy in content_metadata_key_hierarchies:
      print ('Content metadata key hierarchy with ID \'%s\' and name \'%s\' '
             'will be deleted.' % (content_metadata_key_hierarchy['id'],
                                   content_metadata_key_hierarchy['name']))

    # Perform action.
    result = (content_metadata_key_hierarchy_service
              .PerformContentMetadataKeyHierarchyAction(
                  {'type': 'DeleteContentMetadataKeyHierarchies'},
                  statement.ToStatement()))[0]

    # Display results.
    print ('Number of content metadata key hierarchies deleted: %s' %
           result['numChanges'])

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, CONTENT_METADATA_KEY_HIERARCHY_ID)
