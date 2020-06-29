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
from st2common.exceptions import coditationBaseException
from st2common.exceptions.db import coditationDBObjectNotFoundError

__all__ = [
    'TokenNotProvidedError',
    'TokenNotFoundError',
    'TokenExpiredError',
    'TTLTooLargeException',
    'ApiKeyNotProvidedError',
    'ApiKeyNotFoundError',
    'MultipleAuthSourcesError',
    'NoAuthSourceProvidedError',
    'NoNicknameOriginProvidedError',
    'UserNotFoundError',
    'AmbiguousUserError',
    'NotServiceUserError'
]


class TokenNotProvidedError(coditationBaseException):
    pass


class TokenNotFoundError(coditationDBObjectNotFoundError):
    pass


class TokenExpiredError(coditationBaseException):
    pass


class TTLTooLargeException(coditationBaseException):
    pass


class ApiKeyNotProvidedError(coditationBaseException):
    pass


class ApiKeyNotFoundError(coditationDBObjectNotFoundError):
    pass


class ApiKeyDisabledError(coditationDBObjectNotFoundError):
    pass


class MultipleAuthSourcesError(coditationBaseException):
    pass


class NoAuthSourceProvidedError(coditationBaseException):
    pass


class NoNicknameOriginProvidedError(coditationBaseException):
    pass


class UserNotFoundError(coditationBaseException):
    pass


class AmbiguousUserError(coditationBaseException):
    pass


class NotServiceUserError(coditationBaseException):
    pass
