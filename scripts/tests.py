#! /usr/bin/env python3
# coding: utf-8

import plotly
import plotly.graph_objs as go
import json
from covid19 import datasource


data = datasource.get_data()

print(data)
