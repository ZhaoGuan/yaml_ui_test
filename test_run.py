#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import os
import pytest
from module.case_runner import CaseRunner, get_cases
from module.golable_function import config_reader

PATH = os.path.dirname(os.path.abspath(__file__))
temp_path = os.path.abspath(PATH + "/temp")
cases_path = temp_path + "/cases.yml"

get_cases("all", "online")
cases_data = config_reader(cases_path)
run_case_data = []
description_list = []
for case in cases_data:
    run_case_data.append((case["path"], case["source"]))
    if case["description"] is None:
        description_list.append("没有填写描述")
    else:
        description_list.append(case["description"])


@pytest.mark.parametrize("path,source", run_case_data, ids=description_list)
def test_template(path, source):
    cr = CaseRunner(path, source)
    cr.runner()
