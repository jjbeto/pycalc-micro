#!/usr/bin/env python
# communication.py
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

import msgpack
import requests

from shared.error_model import InvalidOperationError, MsgpackInvalidError
from shared.obj_factory import check_type

_LOCATIONS = {
    'evaluate': 'http://localhost:5000/',
    'add': 'http://localhost:5001/',
    'sub': 'http://localhost:5002/',
    'mul': 'http://localhost:5003/',
    'div': 'http://localhost:5004/',
    'pow': 'http://localhost:5005/',
}


def remote_call(json):
    """
    Execute a remote call to evaluate an operation_type
    """
    operation_type = json.get('t')
    if not operation_type or operation_type.lower() not in _LOCATIONS.keys():
        raise InvalidOperationError()

    response = requests.post(_LOCATIONS[operation_type.lower()],
                             data=msgpack.packb(json, raw=False),
                             headers={'Content-Type': 'application/msgpack'})
    return msgpack.unpack(response.content, raw=False)


def get_evaluation(json):
    """
    Get the result operation for one side
    :param json: the object to evaluate
    :param side: the side to be evaluate - 'r' is right and 'l' is left
    """
    if isinstance(json, dict):
        return json if check_type(json, 'num') else remote_call(json)
    else:
        raise InvalidOperationError(f'Invalid node: {json}')


def extract_body(data):
    """
    Extracts the message from data
    """
    try:
        return msgpack.unpackb(data, raw=False)
    except ValueError:
        raise MsgpackInvalidError()
