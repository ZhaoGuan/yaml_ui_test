#!/usr/bin/env python
# coding=utf-8

import functools
import os
import shutil
import tempfile
import base64

from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")


class Extend(object):
    def __init__(self, driver):
        self.driver = driver

    def get_screen_shot_by_element(self, element):
        # 先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(TEMP_FILE)

        # 获取元素bounds
        location = element.location
        size = element.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
        # 截取图片
        image = Image.open(TEMP_FILE)
        new_image = image.crop(box)
        new_image.save(TEMP_FILE)

        return self

    def get_screen_shot_by_custom_size(self, start_x, start_y, end_x, end_y):
        # 自定义截取范围
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(TEMP_FILE)
        new_image = image.crop(box)
        new_image.save(TEMP_FILE)

        return self

    @classmethod
    def write_to_file(cls, dir_path, image_name, form="png"):
        # 将截屏文件复制到指定目录下
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        pic_path = PATH(dir_path + "/" + image_name + "." + form)
        shutil.copyfile(TEMP_FILE, pic_path)
        return pic_path

    @classmethod
    def write_to_base64(cls):
        with open(TEMP_FILE, 'rb') as image:
            image_str = base64.b64encode(image.read())
            image_str = str(image_str, encoding="utf-8")
            # print(image_str)
            return image_str

    @classmethod
    def load_image(cls, image_path):
        # 加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" % image_path)

    # http://testerhome.com/topics/202
    @classmethod
    def same_as(cls, load_image, percent=0):
        # 对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        import math
        import operator

        image1 = Image.open(TEMP_FILE)
        image2 = load_image

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(functools.reduce(operator.add, list(map(lambda a, b: (a - b) ** 2,
                                                                   histogram1, histogram2))) / len(histogram1))
        if differ <= percent:
            return True
        else:
            return False

    def get_screen_shot_by_location(self, x, y, width, height):
        self.driver.get_screenshot_as_file(TEMP_FILE)

        # 获取元素bounds
        box = (x, y, x + width, y + height)

        # 截取图片
        image = Image.open(TEMP_FILE)
        new_image = image.crop(box)
        new_image.save(TEMP_FILE)

        return self

    @classmethod
    def similarity_rate(cls, load_image):
        # 对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        import math
        import operator

        image1 = Image.open(TEMP_FILE)
        image2 = load_image

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(functools.reduce(operator.add, list(map(lambda a, b: (a - b) ** 2,
                                                                   histogram1, histogram2))) / len(histogram1))
        return differ
