#!/usr/bin/env bash
source ${PWD}/shakedown.sh

# cannot accept letters
shakedown POST / -H 'Content-Type: text/plain' -d 'abc'
  status 500
  content_type 'application/json'
  contains 'An unexpected error occurred - Unexpected character: a'

# accepts only text/plain
shakedown POST / -H 'Content-Type: text/html' -d 'abc'
  status 406
  content_type 'application/json'
  contains 'Invalid request type, only text/plain is accepted'

# simple number
shakedown POST / -H 'Content-Type: text/plain' -d ' + 1 '
  status 200
  content_type 'text/plain'
  matches '1.0'

# simple expression
shakedown POST / -H 'Content-Type: text/plain' -d '1 + 1'
  status 200
  content_type 'text/plain'
  matches '2.0'

# sequence expression
shakedown POST / -H 'Content-Type: text/plain' -d '2 / 2 * 2'
  status 200
  content_type 'text/plain'
  matches '2.0'

# expression with sublevels
shakedown POST / -H 'Content-Type: text/plain' -d '(10/10) * (-5+1)'
  status 200
  content_type 'text/plain'
  matches '\-4.0'

# expression with multiple sublevels
shakedown POST / -H 'Content-Type: text/plain' -d '((4x2+2)/(5x2)) * ((5-10)+(10-9))'
  status 200
  content_type 'text/plain'
  matches '\-4.0'

# expression a bit more complex
shakedown POST / -H 'Content-Type: text/plain' -d '26 + { 12 - [ ( 30 - 18) + ( 4 - 1) - 6 ] - 1 }'
  status 200
  content_type 'text/plain'
  matches '28.0'
