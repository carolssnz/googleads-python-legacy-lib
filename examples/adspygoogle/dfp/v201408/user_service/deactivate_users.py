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

"""This code example deactivates a user.

Deactivated users can no longer make requests to the API. The user making the
request cannot deactivate itself. To determine which users exist, run
get_all_users.py."""

__author__ = 'Nicholas Chen'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfpClient
from adspygoogle.dfp import DfpUtils

USER_ID = 'INSERT_USER_ID_TO_DEACTIVATE_HERE'


def main(client, user_id):
  # Initialize appropriate service.
  user_service = client.GetService('UserService', version='v201408')

  # Create query.
  values = [{
      'key': 'userId',
      'value': {
          'xsi_type': 'NumberValue',
          'value': user_id
      }
  }]
  query = 'WHERE id = :userId'

  # Create a filter statement.
  statement = DfpUtils.FilterStatement(query, values)

  # Get users by statement.
  response = user_service.GetUsersByStatement(statement.ToStatement())[0]
  users = response.get('results')

  for user in users:
    print ('User with id \'%s\', email \'%s\', and status \'%s\' will be '
           'deactivated.'
           % (user['id'], user['email'],
              {'true': 'ACTIVE', 'false': 'INACTIVE'}[user['isActive']]))
  print 'Number of users to be deactivated: %s' % len(users)

  # Perform action.
  result = user_service.PerformUserAction({'type': 'DeactivateUsers'},
                                          statement.ToStatement())[0]

  # Display results.
  if result and int(result['numChanges']) > 0:
    print 'Number of users deactivated: %s' % result['numChanges']
  else:
    print 'No users were deactivated.'

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = DfpClient(path=os.path.join('..', '..', '..', '..', '..'))
  main(dfp_client, USER_ID)
