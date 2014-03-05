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

"""This code example creates new content metadata key hierarchies.

To determine which content metadata key hierarchies exist, run
get_all_content_metadata_key_hierarchies.py.

This feature is only available to DFP video publishers.

Tags: ContentMetadataKeyHierarchyService.createContentMetadataKeyHierarchies
"""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.common import Utils

# Set the IDs of the custom targeting keys for the hierarchy.
HIERARCHY_LEVEL_ONE_KEY_ID = 'INSERT_LEVEL_ONE_CUSTOM_TARGETING_KEY_ID_HERE'
HIERARCHY_LEVEL_TWO_KEY_ID = 'INSERT_LEVEL_TWO_CUSTOM_TARGETING_KEY_ID_HERE'


def main(client, hierarchy_level_one_key_id, hierarchy_level_two_key_id):
  # Initialize appropriate service.
  content_metadata_key_hierarchy_service = client.GetService(
      'ContentMetadataKeyHierarchyService', version='v201403')

  hierarchy_level_1 = {
      'customTargetingKeyId': hierarchy_level_one_key_id,
      'hierarchyLevel': '1'
  }

  hierarchy_level_2 = {
      'customTargetingKeyId': hierarchy_level_two_key_id,
      'hierarchyLevel': '2'
  }

  hierarchy_levels = [hierarchy_level_1, hierarchy_level_2]

  # Create content metadata key hierarchy object.
  content_metadata_key_hierarchy = {
      'name': 'Content Metadata Key Hierarchy #%s' % Utils.GetUniqueName(),
      'hierarchyLevels': hierarchy_levels
  }

  content_metadata_key_hierarchies = (
      content_metadata_key_hierarchy_service
      .createContentMetadataKeyHierarchies([content_metadata_key_hierarchy]))

  # Display results.
  for content_metadata_key_hierarchy in content_metadata_key_hierarchies:
    print ('Content metadata key hierarchy with id \'%s\' and name \'%s\''
           ' was created.' % (content_metadata_key_hierarchy['id'],
                              content_metadata_key_hierarchy['name']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, HIERARCHY_LEVEL_ONE_KEY_ID, HIERARCHY_LEVEL_TWO_KEY_ID)
