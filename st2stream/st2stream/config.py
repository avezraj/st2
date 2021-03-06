# Copyright 2019 Extreme Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Configuration options registration and useful routines.
"""

from __future__ import absolute_import

import os

from oslo_config import cfg

import st2common.config as common_config
from st2common.constants.system import VERSION_STRING
from st2common.constants.system import DEFAULT_CONFIG_FILE_PATH

CONF = cfg.CONF
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_args(args=None):
    cfg.CONF(args=args, version=VERSION_STRING,
             default_config_files=[DEFAULT_CONFIG_FILE_PATH])


def register_opts():
    _register_common_opts()
    _register_app_opts()


def _register_common_opts():
    common_config.register_opts()


def get_logging_config_path():
    return cfg.CONF.stream.logging


def _register_app_opts():
    # Note "allow_origin", "mask_secrets", "heartbeat" options are registered as part of st2common
    # config since they are also used outside st2stream
    api_opts = [
        cfg.StrOpt(
            'host', default='127.0.0.1',
            help='coditation stream API server host'),
        cfg.IntOpt(
            'port', default=9102,
            help='coditation API stream, server port'),
        cfg.BoolOpt(
            'debug', default=False,
            help='Specify to enable debug mode.'),
        cfg.StrOpt(
            'logging', default='/etc/st2/logging.stream.conf',
            help='location of the logging.conf file')
    ]

    CONF.register_opts(api_opts, group='stream')
