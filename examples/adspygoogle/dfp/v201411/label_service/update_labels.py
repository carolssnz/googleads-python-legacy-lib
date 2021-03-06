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

"""This code example updates the description of a single label.

To determine which labels exist, run get_all_labels.py. This feature is only
available to DFP premium solution networks."""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils

LABEL_ID = 'INSERT_LABEL_ID_HERE'


def main(client, label_id):
  # Initialize appropriate service.
  label_service = client.GetService('LabelService', version='v201411')

  # Create a statement to select only active labels.
  values = [
      {
          'key': 'labelId',
          'value': {
              'xsi_type': 'NumberValue',
              'value': label_id
          }
      }
  ]
  query = 'WHERE id = :labelId'
  statement = DfpUtils.FilterStatement(query, values)

  # Get labels by filter.
  response = label_service.GetLabelsByStatement(statement.ToStatement())[0]
  labels = response.get('results')

  if labels:
    # Update each local label object by changing the description.
    for label in labels:
      label['description'] = 'These labels are updated.'

    # Update labels remotely.
    labels = label_service.UpdateLabels(labels)

    for label in labels:
      print ('Label with id \'%s\' and name \'%s\' was updated.'
             % (label['id'], label['name']))
  else:
    print 'No labels found to update.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, LABEL_ID)

