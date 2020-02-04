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

from flask import Flask, request

from evaluate.eval_operation import evaluate
from shared.error_handler import errors
from shared.error_model import TextPlainRequestError, RequestBodyMandatoryError

_REGEX_EXTRACT_BODY = re.compile(r'^b\'(.*)?\'$')


def _initialize_error_handlers(application):
    """
    Initialize error handlers
    """
    application.register_blueprint(errors)


def create_app(test_config=None):
    """
    Create an app by initializing components.
    """
    application = Flask(__name__)
    application.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="master-key",
    )
    if test_config:
        application.config.update(test_config)

    _initialize_error_handlers(application)

    @application.route('/', methods=['POST'])
    def post_evaluate():
        if request.content_type != 'text/plain':
            raise TextPlainRequestError()

        body = extract_body(request.get_data())
        evaluation = evaluate(body)
        return str(evaluation), 200, {'Content-Type': 'text/plain; charset=utf-8'}

    return application


def extract_body(data):
    raw_body = str(data)
    groups = _REGEX_EXTRACT_BODY.match(raw_body).groups()
    if len(groups):
        return groups[0]
    else:
        raise RequestBodyMandatoryError()


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
