#! /usr/bin/env python3
# coding: utf-8

from covid19 import datasource
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, world!'

def main():
    rows = datasource.get_data()

    print(rows)


if __name__ == "__main__":
    main()
