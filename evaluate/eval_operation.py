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

import operator
import re
import sys
from collections import namedtuple
from enum import Enum


class TokenType(Enum):
    OP = 1  # Operator
    NUM = 2  # Number
    OPAREN = 3  # Open parenthesis
    CPAREN = 4  # Close parenthesis
    END = 5  # End of input


_FUNCTIONS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,
}

_REGEX_TOKENS = re.compile(r'''
    \s*(?:                      # Optional whitespace, followed by one of
    ([\+\*\/\^\-])              # Operator
    |((?:[1-9]\d*|0)(?:\.\d+)?) # Number
    |(\()                       # Open parenthesis
    |(\))                       # Close parenthesis
    |(.))                       # Any other character is an error
''', re.VERBOSE)

_ESCAPES = {
    '[': '(',
    ']': ')',
    '{': '(',
    '}': ')',
    '–': '-',
    ':': '/',
    '÷': '/',
    'x': '*',
    '²': '^2',
    '³': '^3',
    ' ': ''
}

Token = namedtuple('Token', 'type value')
# Parse tree: either number or binary expression with left operand,
# operator function, and right operand.
Number = namedtuple('Number', 'value')
BinExpr = namedtuple('BinExpr', 'left op right')


def escape(expr):
    """
    Sanitise expr and substitute data according to a dict.
    :param expr: expression
    :return: sanitized expression
    """
    for seq, esc in _ESCAPES.items():
        expr = expr.replace(seq, esc)
    return expr


def tokenize(expr):
    """
    Generate the tokens in the string expr, followed by END.
    :param expr: str with complete expression
    :return: list of tokens
    """
    expr = escape(expr)
    for match in _REGEX_TOKENS.finditer(expr):
        op, num, oparen, cparen, error = match.groups()
        if op:
            yield Token(TokenType.OP, op)
        elif num:
            yield Token(TokenType.NUM, float(num))
        elif oparen:
            yield Token(TokenType.OPAREN, oparen)
        elif cparen:
            yield Token(TokenType.CPAREN, cparen)
        else:
            raise SyntaxError(f'Unexpected character: {error}')
    yield Token(TokenType.END, 'end of input')


def parse(tokens):
    """
    Parse iterable of tokens and return a parse tree.
    :param tokens: list of tokens to be parsed
    :return: tree of operations
    """
    tokens = iter(tokens)  # Ensure we have an iterator.
    token = next(tokens)  # The current token.

    def error(expected):
        """
        Current token failed to match, so raise syntax error.
        :param expected: error to be thrown
        """
        raise SyntaxError(f'Expected \'{expected}\' but found \'{token.value}\'')

    def match(type_, values=None):
        """
        If the current token matches type and (optionally) value, advance to the next token and return True.
        Otherwise leave the current token in place and return False.
        :param type_: type to check
        :param values: possible values to match
        :return: True if type of current token match and is in values
        """
        nonlocal token
        if token.type == type_ and (values is None or token.value in values):
            token = next(tokens)
            return True
        else:
            return False

    def term():
        """
        Parse a term starting at the current token.
        :return: the next token
        """
        nonlocal token
        curr_token = token
        if match(TokenType.NUM):
            return Number(value=curr_token.value)
        elif match(TokenType.OPAREN):
            tree = add_or_sub()
            if match(TokenType.CPAREN):
                return tree
            else:
                error("')'")
        elif token.value in '+-':
            return add_or_sub(Number(value=0.0))
        else:
            error('term')

    def expon():
        """
        Parse an exponential starting at the current token.
        :return: binary expression
        """
        nonlocal token
        left = term()
        curr_token = token
        if match(TokenType.OP, '^'):
            right = expon()
            return BinExpr(left=left, op=_FUNCTIONS[curr_token.value], right=right)
        else:
            return left

    def mul_or_truediv():
        """
        Parse a mul_or_truediv or division starting at the current token.
        :return: binary expression
        """
        nonlocal token
        left = expon()
        curr_token = token
        while match(TokenType.OP, '*/'):
            right = expon()
            left = BinExpr(left=left, op=_FUNCTIONS[curr_token.value], right=right)
            curr_token = token
        return left

    def add_or_sub(left=None):
        """
        Parse an addition or subtraction starting at the current token.
        :param left: if there is just a sign number, a 'left' value is overridden with zero
        :return: binary expression
        """
        nonlocal token
        left = mul_or_truediv() if left is None else left
        curr_token = token
        while match(TokenType.OP, '+-'):
            right = mul_or_truediv()
            left = BinExpr(left=left, op=_FUNCTIONS[curr_token.value], right=right)
            curr_token = token
        return left

    tree = add_or_sub()
    if token.type != TokenType.END:
        error('end of input')
    return tree


def eval_tree(tree):
    """
    Evaluate a parse tree and return the result.
    :param tree: to be evaluated
    :return: final calculation result
    """
    if isinstance(tree, Number):
        return tree.value
    elif isinstance(tree, BinExpr):
        return tree.op(eval_tree(tree.left), eval_tree(tree.right))
    else:
        raise TypeError(f'Expected tree but found {type(tree).__name__}')


def evaluate(*expr):
    """
    Evaluate an expression and return the result.
    :param expr: an expression to be calculated
    :return: final result
    """
    if isinstance(expr, list) or isinstance(expr, tuple):
        expr = ''.join(str(each) for each in expr)
    elif not isinstance(expr, str):
        expr = str(expr)
    tokens = tokenize(str(expr))
    tree = parse(tokens)
    return eval_tree(tree)


if __name__ == '__main__':
    args = sys.argv[1:]  # first arg is always __main__
    if len(args):
        print(evaluate(args))
    else:
        print('Please give an expression to be calculated')
