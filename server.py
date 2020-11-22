#!/usr/bin/python3
# -*- coding: utf-8 -*-
from api_setup import create_api

app = create_api()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

