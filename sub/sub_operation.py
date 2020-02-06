#!/usr/bin/env python
# sub_operation.py
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

from shared.communicator import get_evaluation
from shared.error_model import InvalidOperationError, BadRequestError
from shared.obj_factory import get_number, check_type


def sub(json):
    """
    left - right
    """
    if not json.get('t') or json.get('t') != 'sub':
        raise InvalidOperationError('Sub operation was expected')

    left = __evaluation(json, 'l')
    right = __evaluation(json, 'r')

    return get_number(left.get('v') - right.get('v'))


def __evaluation(json, side):
    """
    if current operation is on a side, operate it from local, otherwise call remote evaluation
    """
    if not isinstance(json, dict):
        raise BadRequestError()

    node = json['v'].get(side)
    result = sub(node) if check_type(node, 'sub') else get_evaluation(node)
    if not check_type(result, 'num'):
        raise InvalidOperationError(f'Cannot process operation for node {result}')

    return result
