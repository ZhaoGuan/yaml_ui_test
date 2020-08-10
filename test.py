#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import os
from module.case_runner import CaseRunner

PATH = os.path.dirname(os.path.abspath(__file__))
example_path = PATH + "/cases/example.yml"
cr = CaseRunner(example_path)
cr.runner()
