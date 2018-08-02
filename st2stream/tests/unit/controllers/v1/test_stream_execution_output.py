# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import eventlet

from six.moves import http_client

from st2common.constants import action as action_constants
from st2common.models.db.execution import ActionExecutionDB
from st2common.models.db.execution import ActionExecutionOutputDB
from st2common.persistence.execution import ActionExecution
from st2common.persistence.execution import ActionExecutionOutput
from st2common.util import date as date_utils

from st2common.stream.listener import get_listener

from .base import FunctionalTest

__all__ = [
    'ActionExecutionOutputStreamControllerTestCase'
]


class ActionExecutionOutputStreamControllerTestCase(FunctionalTest):
    def test_get_one_id_last_no_executions_in_the_database(self):
        ActionExecution.query().delete()

        resp = self.app.get('/v1/executions/last/output', expect_errors=True)
        self.assertEqual(resp.status_int, http_client.BAD_REQUEST)
        self.assertEqual(resp.json['faultstring'], 'No executions found in the database')

    def test_get_output_running_execution(self):
        # Retrieve lister instance to avoid race with listener connection not being established
        # early enough for tests to pass.
        # NOTE: This only affects tests where listeners are not pre-initialized.
        listener = get_listener(name='execution_output')
        eventlet.sleep(1.0)

        # Test the execution output API endpoint for execution which is running (blocking)
        status = action_constants.LIVEACTION_STATUS_RUNNING
        timestamp = date_utils.get_datetime_utc_now()
        action_execution_db = ActionExecutionDB(start_timestamp=timestamp,
                                                end_timestamp=timestamp,
                                                status=status,
                                                action={'ref': 'core.local'},
                                                runner={'name': 'run-local'},
                                                liveaction={'ref': 'foo'})
        action_execution_db = ActionExecution.add_or_update(action_execution_db)

        output_params = dict(execution_id=str(action_execution_db.id),
                             action_ref='core.local',
                             runner_ref='dummy',
                             timestamp=timestamp,
                             output_type='stdout',
                             data='stdout before start\n')

        # Insert mock output object
        output_db = ActionExecutionOutputDB(**output_params)
        ActionExecutionOutput.add_or_update(output_db, publish=False)

        def insert_mock_data():
            output_params['data'] = 'stdout mid 1\n'
            output_db = ActionExecutionOutputDB(**output_params)
            ActionExecutionOutput.add_or_update(output_db)

        # Since the API endpoint is blocking (connection is kept open until action finishes), we
        # spawn an eventlet which eventually finishes the action.
        def publish_action_finished(action_execution_db):
            # Insert mock output object
            output_params['data'] = 'stdout pre finish 1\n'
            output_db = ActionExecutionOutputDB(**output_params)
            ActionExecutionOutput.add_or_update(output_db)

            eventlet.sleep(1.0)

            # Transition execution to completed state so the connection closes
            action_execution_db.status = action_constants.LIVEACTION_STATUS_SUCCEEDED
            action_execution_db = ActionExecution.add_or_update(action_execution_db)

        eventlet.spawn_after(0.2, insert_mock_data)
        eventlet.spawn_after(1.5, publish_action_finished, action_execution_db)

        # Retrieve data while execution is running - endpoint return new data once it's available
        # and block until the execution finishes
        resp = self.app.get('/v1/executions/%s/output' % (str(action_execution_db.id)),
                            expect_errors=False)
        self.assertEqual(resp.status_int, 200)

        events = self._parse_response(resp.text)
        self.assertEqual(len(events), 3)
        self.assertEqual(events[0]['data'], 'stdout before start\n')
        self.assertEqual(events[1]['data'], 'stdout mid 1\n')
        self.assertEqual(events[2]['data'], 'stdout pre finish 1\n')

        # Once the execution is in completed state, existing output should be returned immediately
        resp = self.app.get('/v1/executions/%s/output' % (str(action_execution_db.id)),
                            expect_errors=False)
        self.assertEqual(resp.status_int, 200)

        events = self._parse_response(resp.text)
        self.assertEqual(len(events), 3)
        self.assertEqual(events[0]['data'], 'stdout before start\n')
        self.assertEqual(events[1]['data'], 'stdout mid 1\n')
        self.assertEqual(events[2]['data'], 'stdout pre finish 1\n')

        listener.shutdown()

    def test_get_output_finished_execution(self):
        # Test the execution output API endpoint for execution which has finished
        for status in action_constants.LIVEACTION_COMPLETED_STATES:
            # Insert mock execution and output objects
            status = action_constants.LIVEACTION_STATUS_SUCCEEDED
            timestamp = date_utils.get_datetime_utc_now()
            action_execution_db = ActionExecutionDB(start_timestamp=timestamp,
                                                    end_timestamp=timestamp,
                                                    status=status,
                                                    action={'ref': 'core.local'},
                                                    runner={'name': 'run-local'},
                                                    liveaction={'ref': 'foo'})
            action_execution_db = ActionExecution.add_or_update(action_execution_db)

            for i in range(1, 6):
                stdout_db = ActionExecutionOutputDB(execution_id=str(action_execution_db.id),
                                                    action_ref='core.local',
                                                    runner_ref='dummy',
                                                    timestamp=timestamp,
                                                    output_type='stdout',
                                                    data='stdout %s\n' % (i))
                ActionExecutionOutput.add_or_update(stdout_db)

            for i in range(10, 15):
                stderr_db = ActionExecutionOutputDB(execution_id=str(action_execution_db.id),
                                                    action_ref='core.local',
                                                    runner_ref='dummy',
                                                    timestamp=timestamp,
                                                    output_type='stderr',
                                                    data='stderr %s\n' % (i))
                ActionExecutionOutput.add_or_update(stderr_db)

            resp = self.app.get('/v1/executions/%s/output' % (str(action_execution_db.id)),
                                expect_errors=False)
            self.assertEqual(resp.status_int, 200)

            events = self._parse_response(resp.text)
            self.assertEqual(len(events), 10)
            self.assertEqual(events[0]['data'], 'stdout 1\n')
            self.assertEqual(events[9]['data'], 'stderr 14\n')

            # Verify "last" short-hand id works
            resp = self.app.get('/v1/executions/last/output', expect_errors=False)
            self.assertEqual(resp.status_int, 200)

            events = self._parse_response(resp.text)
            self.assertEqual(len(events), 10)

    def _parse_response(self, response):
        """
        Parse event stream response and return a list of events.
        """
        events = []

        lines = response.strip().split('\n')
        for line in lines:
            if 'data:' in line:
                event_data = line[line.find('data: ') + len('data :'):].strip()

                if len(event_data.strip("'")) == 0:
                    # Skip EOF events:
                    continue

                event = json.loads(event_data)
                events.append(event)

        return events
