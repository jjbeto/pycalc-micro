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

import re

import msgpack
from flask import Flask, request

from mul.mul_operation import mul
from shared.communicator import extract_body
from shared.error_handler import initialize_error_handlers
from shared.error_model import MsgpackRequestError

_REGEX_EXTRACT_BODY = re.compile(r'^b\'(.*)?\'$')


def create_app(test_config=None):
    """
    Create an app by initializing components.
    """
    application = Flask(__name__)
    if test_config:
        application.config.update(test_config)

    initialize_error_handlers(application)

    @application.route('/', methods=['POST'])
    def post_mul():
        if request.content_type != 'application/msgpack':
            raise MsgpackRequestError()

        operation = extract_body(request.get_data())
        result = mul(operation)

        return msgpack.packb(result), 200, {'Content-Type': 'application/msgpack'}

    return application


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
