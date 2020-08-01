#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from module.web_actions import WebAction


class Customize:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.web_action = WebAction(webdriver)
