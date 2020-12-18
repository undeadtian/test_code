# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : web_script.py
@Author  : 王白熊
@Data    ： 2020/12/17 16:37
"""
import time
import os
from project.internal_reference_flush.browser_engine import BrowserEngine
from project.internal_reference_flush.pages import LoginHomePage
from project.internal_reference_flush.pages import ReferencePage
from common.Log import Logger

logger = Logger('reference_flush').getlog()


def get_reference_info(camera_no):
    browse = BrowserEngine()
    driver = browse.open_browser()
    Login_page = LoginHomePage(driver)
    Login_page.set_username()
    Login_page.set_password()
    Login_page.click_login()
    page_url = 'http://172.16.3.2:8090/pages/viewpage.action?pageId=6455589'
    driver.get(page_url)
    reference_page = ReferencePage(driver)
    reference_page.get_index(camera_no)
    sn_no = reference_page.get_sn_no()
    reference_page.download_json()
    driver.quit()
    if os.path.exists(os.path.join(r'C:\Users\Admin\Downloads', r'{}.json'.format(camera_no))):
        return sn_no
    else:
        exit(-1)

    # C:\Users\Admin\Downloads
    # //*[@id="table-joiner-1606908769696_1839827944"]/div[1]/div/table/tbody/tr[1]/td[5]
    # //*[@id="table-joiner-1606908769696_1839827944"]/div[1]/div/table/tbody/tr[1]/td[4]
    # //*[@id="table-joiner-1606908769696_1839827944"]/div[1]/div/table/tbody/tr[1]/td[9]/a

if __name__ == '__main__':
    a= get_reference_info(322)
    print(a)