from flask import Flask, redirect, request,  abort
from urlparse import urlparse

import simplejson as json
import string
import random

app = Flask(__name__)
urls = {}

ALPHANUMERIC = string.ascii_uppercase + string.ascii_lowercase + string.digits
CODE_LENGTH = 6

def create_short_code():
    random.seed()
    short_code = ''.join(random.choice(ALPHANUMERIC) for x in range(CODE_LENGTH))
    return short_code
    
@app.route('/shorten_url', methods=['POST'])
def shorten():
    try:
        data = request.json
        long_url = data['long_url']
        custom_short_code = data.get('custom_short_code', None)
    except Exception:
        abort(400, 'Malformed request or Invalid payload: {custom_short_code(optional): ..., long_url:...}')

    #verify custom code availability
    if custom_short_code is not None and urls.get(custom_short_code) is not None:
        abort(400, 'Custom code cannot be assigned')

    #create code if not provided
    if custom_short_code is None:
        custom_short_code = create_short_code()

    success = False
    if urls.get(custom_short_code) is None:
        if not urlparse(long_url).scheme:
            long_url = '//' + long_url    

        urls[custom_short_code] = long_url
        success = True

    return '{"success": "%s", "short_code": "%s"}' % (success, custom_short_code)

@app.route('/<short_code>', methods=['GET'])
def map(short_code):
    try:
        long_url = urls[short_code]
    except Exception:
        abort(400, 'Invalid short code')

    return redirect(long_url, 302)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

