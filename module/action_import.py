#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from module.web_actions import WebAction
from customize_function.customize_action import Customize


class ActionImport:
    def __init__(self, webdriver):
        self.base_function = WebAction(webdriver)
        self.customize_function = Customize(webdriver)
        self.base_function_list = list(filter(
            lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self.base_function, m)),
            dir(self.base_function)))
        self.customize_function_list = list(filter(
            lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self.base_function, m)),
            dir(self.base_function)))
        self.customize_function = Customize(webdriver)

    def use_base_function(self, func_name, kwargs):
        """
        基础的操作方法主要封装简单常用的方法，尽量不复杂后边可以使用更复杂的调用类方法来弥补
        :param func_name: WebAction下的方法名称
        :param kwargs: 对应方法名的传入参数，使用字典形传入
        eg: 方法参数: value,message
            写法: {"value":value,"message":message}
        :return: 直接执行对应方法
        """
        func = getattr(self.base_function, func_name)
        if isinstance(kwargs, dict):
            return func(**kwargs)
        elif isinstance(kwargs, list):
            return func(*kwargs)
        else:
            return func()

    def use_customize_function(self, func_name, kwargs):
        """
        这里主要是使用自定义的方法为了跟框架解耦，可以直接使用WebAction的方法来组成新方法。
        :param func_name: Customize下的方法名称
        :param kwargs: 对应方法名的传入参数，使用字典形传入
        eg: 方法参数: value,message
            写法: {"value":value,"message":message}
        :return: 直接执行对应方法
        """
        if func_name not in self.customize_function_list:
            assert False, "Customize中没有对应的方法" + func_name
        func = getattr(self.customize_function, func_name)
        if isinstance(kwargs, dict):
            return func(**kwargs)
        elif isinstance(kwargs, list):
            return func(*kwargs)
        else:
            return func()

    def use_function(self, func_name, kwargs):
        if func_name in self.base_function_list:
            self.use_base_function(func_name, kwargs)
        else:
            self.use_customize_function(func_name, kwargs)


if __name__ == "__main__":
    ai = ActionImport("123")
    print(ai.base_function_list)
    ai.use_base_function("test", {"a": "a", "b": "b", "c": "c"})
