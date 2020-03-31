#! /usr/bin/env python3
# coding: utf-8

from covid19 import controller

if __name__ == "__main__":
    controller.app.run(debug=True, host='0.0.0.0')
