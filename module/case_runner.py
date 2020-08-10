#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from module.golable_function import config_reader, config_data_path, save_config
from module.selenium_driver import BrowserDriver
from module.web_actions import WebAction
from module.action_import import ActionImport
import os
import yaml

PATH = os.path.dirname(os.path.abspath(__file__))
CASES_PATH = os.path.abspath(PATH + "/../cases")


def dir_list(path, all_files):
    file_list = os.listdir(path)
    for filename in file_list:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dir_list(filepath, all_files)
        else:
            all_files.append(filepath)
    return all_files


def select_case_folder(options):
    if options == "all":
        result = []
        path = CASES_PATH
        return dir_list(path, result)
    else:
        return case_list(options)


def case_list(folder_name):
    folder_path = PATH + "/../case/" + folder_name
    folder_list = []
    try:
        dir_list(folder_path, folder_list)
    except Exception as e:
        print(e)
        print("文件夹填写错误")
        assert False
    result = [folder for folder in folder_list]
    return result


def get_cases(dir_name, source="online"):
    cases = select_case_folder(dir_name)
    result = []
    for case in cases:
        if "!" not in case:
            data = config_reader(case)
            description = data["DESCRIPTION"]
            result.append({"path": case, "description": description, "source": source})
    temp_path = os.path.abspath(PATH + "/../temp")
    try:
        os.mkdir(temp_path)
    except:
        pass
    cases_path = temp_path + "/cases.yml"
    save_config(result, cases_path)


class CaseRunner:
    def __init__(self, case_path, source="online"):
        self.config = config_reader(case_path)
        self.title = self.config["TITLE"]
        self.description = self.config["DESCRIPTION"]
        self.hots = self.config["HOST"]
        try:
            self.hots = self.hots[source]
        except:
            self.hots = None
        if self.hots is None:
            self.url = self.config["URL"]
        else:
            self.path = self.config["PATH"]
            if self.path is None:
                self.url = self.hots
            else:
                self.url = self.hots + self.path
        self.actions = self.config["ACTIONS"]
        self.bd = BrowserDriver()
        self.webdriver = self.bd.chrome_browser_driver()
        self.wa = WebAction(self.webdriver)
        self.wa.url(self.url)
        self.ai = ActionImport(self.webdriver)

    def runner(self):
        try:
            self.__runner()
            self.bd.close_chrome_browser_driver()
        except Exception as error:
            error.__init__ = self.bd.close_chrome_browser_driver()
            raise Exception from error

    def __runner(self):
        for action in self.actions:
            self.do_action(action)

    def do_action(self, data):
        global action_assert_data, action_assert_type
        action_type = data["TYPE"]
        if "DATA" in data.keys():
            action_data = data["DATA"]
        else:
            action_data = None
        if "ASSERT" in data.keys():
            action_assert = data["ASSERT"]
            action_assert_type = action_assert["TYPE"]
            action_assert_data = action_assert["DATA"]
        else:
            action_assert = None
        # if isinstance(action_data, dict):
        #     element_func = self.ai.use_function(action_type, action_data)
        # else:
        #     element_func = self.ai.use_function(action_type, action_data)
        element_func = self.ai.use_function(action_type, action_data)
        if action_assert is not None:
            if isinstance(action_assert_data, list):
                data = [element_func]
                [data.append(i) for i in action_assert_data]
                self.ai.use_function(action_assert_type, data)
            else:
                data = {"func": element_func}
                for k, v in action_assert_data.items():
                    data[k] = v
                self.ai.use_function(action_assert_type, data)
