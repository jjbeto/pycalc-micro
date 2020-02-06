#!/usr/bin/env python

# main.py
#
# Copyright 2020 Jose Jouberto Fonseca Lopes.
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
# limitations under the License


class ApiError(Exception):
    """
    Base exception with a status code and message
    """

    def __init__(self, status_code, message):
        self.__status_code = status_code
        self.__message = message

    @property
    def status_code(self):
        return str(self.__status_code)

    @property
    def message(self):
        return str(self.__message)


class TextPlainRequestError(ApiError):
    """
    406 Invalid request type, only text/plain is accepted
    """

    def __init__(self):
        super().__init__(406, 'Invalid request type, only text/plain is accepted')


class MsgpackRequestError(ApiError):
    """
    406 Invalid request type, only application/msgpack is accepted
    """

    def __init__(self):
        super().__init__(406, 'Invalid request type, only application/msgpack is accepted')


class MsgpackInvalidError(ApiError):
    """
    400 BBad Request: not possible to decode message
    """

    def __init__(self):
        super().__init__(400, 'Bad Request: not possible to decode message')


class BadRequestError(ApiError):
    """
    400 BBad Request: not possible to decode message
    """

    def __init__(self):
        super().__init__(400, 'Bad Request: message is not correct')


class RequestBodyMandatoryError(ApiError):
    """
    400 Bad Request - request body is mandatory
    """

    def __init__(self):
        super().__init__(406, 'Invalid request type, only text/plain is accepted')


class InvalidOperationError(ApiError):
    """
    500 Internal Error - operation is invalid
    """

    def __init__(self, msg=None):
        super().__init__(406, f'Internal Error: {msg}' if msg else 'Internal Error: operation is invalid')
