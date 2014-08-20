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

"""This code example gets all content metadata key hierarchies.

This feature is only available to DFP video publishers.

Tags: ContentMetadataKeyHierarchyService.getContentMetadataKeyHierarchiesByStatement
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


def main(client):
  # Initialize appropriate service.
  content_metadata_key_hierarchy_service = client.GetService(
      'ContentMetadataKeyHierarchyService', version='v201408')

  # Create statement object to select all content.
  statement = DfpUtils.FilterStatement()

  # Get content by statement.
  while True:
    response = (content_metadata_key_hierarchy_service
                .GetContentMetadataKeyHierarchiesByStatement(
                    statement.ToStatement())[0])
    content_metadata_key_hierarchies = response.get('results')
    if content_metadata_key_hierarchies:
      # Display results.
      for content_metadata_key_hierarchy in content_metadata_key_hierarchies:
        print ('Content metadata key hierarchyy with id \'%s\' and name \'%s\''
               ' was found.' % (content_metadata_key_hierarchy['id'],
                                content_metadata_key_hierarchy['name']))
      statement.IncreaseOffsetBy(DfpUtils.PAGE_LIMIT)
    else:
      break

  print '\nNumber of results found: %s' % response['totalResultSetSize']

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
