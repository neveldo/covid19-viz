#! /usr/bin/env python3
# coding: utf-8

from covid19 import server

if __name__ == "__main__":
    server.app.run(debug=True, host='0.0.0.0')
