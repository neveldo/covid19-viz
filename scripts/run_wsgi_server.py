#! /usr/bin/env python3
# coding: utf-8

from covid19 import controller

"""
Run the app with uwsgi and nginx
"""
app = controller.app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)
