# -*- coding: utf-8 -*-
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

from __future__ import absolute_import
import os.path

from setuptools import setup
from setuptools import find_packages

from dist_utils import fetch_requirements
from dist_utils import apply_vagrant_workaround

from mistral_v2 import __version__

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_FILE = os.path.join(BASE_DIR, 'requirements.txt')

install_reqs, dep_links = fetch_requirements(REQUIREMENTS_FILE)

apply_vagrant_workaround()
setup(
    name='coditation-runner-mistral-v2',
    version=__version__,
    description=('Mistral v2 workflow action runner for coditation event-driven '
                 'automation platform'),
    author='coditation',
    author_email='info@coditation.com',
    license='Apache License (2.0)',
    url='https://coditation.com/',
    install_requires=install_reqs,
    dependency_links=dep_links,
    test_suite='tests',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['setuptools', 'tests']),
    package_data={'mistral_v2': ['runner.yaml']},
    scripts=[],
    entry_points={
        'st2common.runners.runner': [
            'mistral-v2 = mistral_v2.mistral_v2',
        ],
        'st2common.runners.query': [
            'mistral-v2 = mistral_v2.query',
        ],
        'st2common.runners.callback': [
            'mistral-v2 = mistral_v2.callback',
        ],
    }
)
