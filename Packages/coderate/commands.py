#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : JinHua
# @Date    : 2020-10-09 17:58:46
# @Contact : hgu_autotestc103@fiberhome.com
# @Site    :
# @File    : commands.py
# @Software: PyCharm
# @Desc    :
# @license : Copyright(C), cienet

import re
import sublime
import sublime_plugin

PLUGIN_NAME = 'CodeRate'

# class CodeRateCommand(sublime_plugin.WindowCommand):
#     """docstring for CodeRate"""

#     def run(self, view):
#         contents = self.view.substr(sublime.Region(0, self.view.size()))
#         print(contents)

def get_number(char):
    """
    判断字符串中，中文的个数
    :param char: 字符串
    :return:
    """
    count = 0
    for item in char:
        # 判断字符是否为中文字符
        if 0x4E00 <= ord(item) <= 0x9FA5:
            count += 1
    return count


class CodeRateListener(sublime_plugin.EventListener):
    """docstring for CodeRateListener"""

    # def on_post_save(self, view):
    #     '''
    #     保存文件时计算注释率.
    #     '''
    #     contents = view.substr(sublime.Region(0, view.size()))
    #     serial_num_sum, code_sum, rate = self.get_noderate(contents)
    #     self.set_status(view, '【%d %d %d%%】' % (serial_num_sum, code_sum, rate))

    def on_load(self, view):
        '''
        加载文件时计算注释率.
        '''
        contents = view.substr(sublime.Region(0, view.size()))
        serial_num_sum, code_sum, rate = self.get_noderate(contents)
        self.set_status(view, '【%d %d %d%%】' % (serial_num_sum, code_sum, rate))

    def on_modified(self, view):
        '''
        修改文件时计算注释率.
        '''
        contents = view.substr(sublime.Region(0, view.size()))
        serial_num_sum, code_sum, rate = self.get_noderate(contents)
        self.set_status(view, '【%d %d %d%%】' % (serial_num_sum, code_sum, rate))

    def set_status(self, view, message):
        view.set_status('test', message)

    def get_number(self, char):
        """
        判断字符串中，中文的个数
        :param char: 字符串
        :return:
        """
        count = 0
        for item in char:
            # 判断字符是否为中文字符
            if 0x4E00 <= ord(item) <= 0x9FA5:
                count += 1
        return count

    def get_noderate(self, contents):
        """
        校验py文件注释比
        :param user_path: py文件全路径
        :return:
        """
        code_sum = 0

        my_lines = contents.split('\n')
        # print(my_lines)
        ser = 0
        serial_num_list = []

        # 逐行检索文本中是否包含注释
        for serial_num, line in enumerate(my_lines):
            # print(serial_num, line)
            # print(20 * '+')
            if line.strip() != "":  # 过滤空行
                serial_num = serial_num + 1

                if re.match(r".*\"\"\".*", line):  # 记录文档注释行行数
                    serial_num_list.append(serial_num)

                elif "#" in line:  # 记录单行注释行数
                    linelist = line.split('#')
                    node1 = linelist[1]
                    nodenum = get_number(node1)
                    if nodenum > 4:  # 单行注释中文个数不小于5个为有效注释
                        ser += 1
                # print(serial_num)

                code_sum += 1

        serial_num_sum2 = 0

        try:  # 计算文本注释
            for ser_num, value in enumerate(serial_num_list):
                if ser_num % 2 == 0:
                    top_num = value
                else:
                    end_num = value
                    # 行尾与行头行数相减即为文档注释所占行数，累加所有文档注释
                    serial_num_sum2 += (int(end_num) - int(top_num) + 1)
        except Exception as ex:
            print(ex)
            print("%s源码注释不规范!自动跳过!" % user_path)

        # serial_num_sum = ser + serial_num_sum2  # 叠加两种注释行数
        serial_num_sum = ser # 只计算单行注释
        if code_sum != 0:
            exp_rate = 100 * (serial_num_sum / code_sum)  # 计算注释比
        else:
            exp_rate = 0
        # print("=======" * 10)
        # print("注释的行数为:%d,总行数为%d|注释率为%d%%" % (serial_num_sum, code_sum, exp_rate))
        return serial_num_sum, code_sum, exp_rate


