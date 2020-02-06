#!/usr/bin/env python
# obj_factory.py
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


def get_operation(op, left, right):
    return {'t': op, 'v': {'l': left, 'r': right}}


def get_number(value):
    return {'t': 'num', 'v': value}


def check_type(json, op):
    return json.get('t', '') == op
