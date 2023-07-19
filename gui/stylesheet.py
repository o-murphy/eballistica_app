# -*- coding: utf-8 -*-

import traceback


def load_qss(file_name):
    """use setStylesheet(load_qss(filename))"""
    try:
        with open(file_name, 'r') as fh:
            return fh.read()
    except FileNotFoundError as err:
        print(traceback.format_exc())
        return ''


def main_app_qss():
    """use setStylesheet(main_app_qss())"""
    try:
        with open('qss/application.qss', 'r') as fh:
            app_qss = fh.read()
        with open('qss/profiles_table.qss', 'r') as fh:
            tab_qss = fh.read()
        return tab_qss + app_qss
    except FileNotFoundError as err:
        print(traceback.format_exc())
        return ''
