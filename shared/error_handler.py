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

"""
Application error handlers.
source: https://opensource.com/article/17/3/python-flask-exceptions
"""
from flask import Blueprint, jsonify

from shared.error_model import ApiError

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(ApiError)
def handle_error(error):
    response = {
        "error": {
            "message": error.message
        }
    }
    return jsonify(response), error.status_code


@errors.app_errorhandler(Exception)
def handle_unexpected_error(error):
    status_code = 500
    response = {
        "error": {
            "message": f"An unexpected error occurred - {error}"
        }
    }
    return jsonify(response), status_code
