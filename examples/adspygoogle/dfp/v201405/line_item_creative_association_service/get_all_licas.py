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

"""This code example gets all line item creative associations (LICA).

To create LICAs, run create_licas.py or associate_creative_set_to_line_item.py.
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
  lica_service = client.GetService(
      'LineItemCreativeAssociationService', version='v201405')

  # Create a filter statement.
  statement = DfpUtils.FilterStatement()

  # Get line items by statement.
  while True:
    response = lica_service.GetLineItemCreativeAssociationsByStatement(
        statement.ToStatement())[0]
    licas = response.get('results')
    if licas:
      # Display results.
      for lica in licas:
        if 'creativeSetId' in lica:
          print ('LICA with line item ID \'%s\', creative set ID \'%s\', and '
                 'status \'%s\' was found.' %
                 (lica['lineItemId'], lica['creativeSetId'], lica['status']))
        else:
          print ('LICA with line item ID \'%s\', creative ID \'%s\', and status'
                 ' \'%s\' was found.' % (lica['lineItemId'], lica['creativeId'],
                                         lica['status']))

  print '\nNumber of results found: %s' % response['totalResultSetSize']

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client)
