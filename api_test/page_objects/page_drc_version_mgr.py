from api_test.base_page.homepage import HomePage
from common.Log import Logger

logger = Logger("DrcVerMgrPage").getlog()


class DrcVerMgrPage(HomePage):

    # 填入版本名称 后面还有一个函数input_version_name 容易混淆！！！
    def input_drc_version_name(self, version_name):
        input_version_link = 'xpath=>//*[@id="Term"]'
        # input_version_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[1]/form/div[1]/input'
        self.type(input_version_link, version_name)

    # 点击查询版本
    def qry_version_click(self):
        qry_version_link = 'xpath=>//*[@id="btn_query"]'
        self.click(qry_version_link)

    # 点击查看版本ftp信息
    def version_ftp_qry_click(self):
        qry_version_ftp_link = 'xpath=>//*[@id="btn_ftpquery"]'
        self.click(qry_version_ftp_link)

    # 是否存在输入弹窗
    # def is_exist_prompt(self):
    #     try:
    #         self.find_element('xpath=>//*[@id="saveftp"]')
    #         logger.info("弹出保存ftp版本信息弹窗")
    #         return True
    #     except Exception as e:
    #         logger.info("未弹保存ftp版本信息弹窗")
    #         return False
    def is_prompt_visible_ftp(self):
        selector = '//*[@id="saveftp"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出存ftp版本信息弹窗%s" % ret)
        return ret

    # 输入ftp域名
    def input_ftp_domain_name(self, domain_name):
        set_ftp_domain_link = 'xpath=>//*[@id="ftpAddress"]'
        self.type(set_ftp_domain_link, domain_name)

    # 输入ftp端口
    def input_ftp_port(self, ftp_port):
        set_ftp_port_link = 'xpath=>//*[@id="ftpPort"]'
        self.type(set_ftp_port_link, ftp_port)

    # 输入ftp用户名
    def input_ftp_user(self, username):
        set_ftp_user_link = 'xpath=>//*[@id="ftpUserName"]'
        self.type(set_ftp_user_link, username)

    # 输入ftp密码
    def input_ftp_password(self, password):
        set_ftp_password_link = 'xpath=>//*[@id="ftpPassword"]'
        self.type(set_ftp_password_link, password)

    # 点击关闭
    def close_window_click(self):
        close_window_link = 'link_text=>"关闭"'
        self.click(close_window_link)

    # 点击保存配置信息
    def save_cfg_click(self):
        save_cfg_link = 'xpath=>//*[@id="btn_saveftp"]'
        self.click(save_cfg_link)

    # 点击刷新
    def refresh_click(self):
        refresh_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[2]/button'
        self.click(refresh_link)

    # 点击全屏
    def full_screen_click(self):
        full_screen_link = 'xpath=>/html/body/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[2]/div/button'
        self.click(full_screen_link)

    # 点击全选
    def all_election_click(self):
        select_all_click = 'xpath=//*[@id="tb_list"]/thead/tr/th[1]/div[1]/label/input'
        self.click(select_all_click)

    # 选择指定唯一标识设备
    # def version_select_click(self, version_no):
    #     for i in range(1, 10):
    #         choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
    #         if self.find_element(choose_box_link_temp).text == version_no:
    #             choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
    #             self.click(choose_box_link)
    #             logger.info("点击指定版本号备成功 version_no:%u" % str(version_no))
    #             return i
    #     logger.info("点击指定版本号失败 version_no:%u" % str(version_no))
    #     i = 0
    #     return i
    # 选择指定版本编号
    # '//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
    def version_id_select_click(self, ver_id):
        for i in range(1, 12):
            choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[2]'
            try:
                record_version_id = self.find_element(choose_box_link_temp).text
                if record_version_id == str(ver_id):
                    choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr[' + str(i) + ']/td[1]/label/input'
                    self.click(choose_box_link)
                    logger.info("点击版本记录编号成功 ver_id:%s" % str(ver_id))
                    return i
            except ValueError:
                logger.info("点击版本记录编号失败 ver_id:%s" % str(ver_id))
                i = 0
                return i

    # 选择指定版本编号 先进行版本查询后只剩下一个选项时用这个函数勾选
    def version_id_select_click_single(self, ver_id='0'):
        choose_box_link_temp = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[2]'
        try:
            if self.find_element(choose_box_link_temp).text == str(ver_id) or str(ver_id) == '0':
                choose_box_link = 'xpath=>//*[@id="tb_list"]/tbody/tr/td[1]/label/input'
                self.click(choose_box_link)
                logger.info("点击指定版本记录编号成功 ver_id:%s" % str(ver_id))
                return True
            else:
                logger.error("点击指定版本记录编号失败 ver_id:%s" % str(ver_id))
                return False
        except Exception as e:
            logger.error("没有指定名称的版本,%s" % format(e))
            raise False

    # 点击新增版本入库
    def version_add_click(self):
        version_add_link = 'xpath=>//*[@id="btn_importVersion"]'
        self.click(version_add_link)

    # 是否存在输入弹窗 新增版本入库弹窗和修改版本弹窗一致
    # def is_exist_prompt2(self):
    #     try:
    #         self.find_element('xpath=>//*[@id="drcAddNewVersionInfoModalLabel"]')
    #         logger.info("弹出版本入库设置弹窗")
    #         return True
    #     except Exception as e:
    #         logger.info("未弹出版本入库设置弹窗")
    #         return False
    def is_prompt_visible_add(self):
        selector = '//*[@id="drcAddNewVersionInfoModalLabel"]'
        ret = self.is_visible(selector)
        logger.info("是否弹出新增版本入库设置弹窗%s" % ret)
        return ret

    # 输入drc版本名称
    def input_version_name(self, version_name):
        input_version_name_link = 'xpath=>//*[@id="versionName"]'
        self.type(input_version_name_link, version_name)

    # 输入上传者名称
    def input_version_author(self, author):
        input_version_author_link = 'xpath=>//*[@id="uploadUser"]'
        self.type(input_version_author_link, author)

    # 输入上传时间
    def input_version_time(self, time):
        input_version_author_link = 'xpath=>//*[@id="tUploadTime"]'
        self.type(input_version_author_link, time)

    # 输入版本所在路径
    def input_version_path(self, version_path):
        input_version_path_link = 'xpath=>//*[@id="uploadSwDir"]'
        self.type(input_version_path_link, version_path)

    # # 点击关闭
    # def close_window_click2(self):
    #     close_window_link = 'xpath=>//*[@id="drcAddNewVersionInfoModal"]/div/div/div[3]/button[1]'
    #     self.click(close_window_link)

    # 点击执行版本入库
    def version_upload_click(self):
        version_upload_link = 'xpath=>//*[@id="btn_uploadeversion"]'
        self.click(version_upload_link)

    # 点击修改版本信息
    def version_mod_click(self):
        version_mod_link = 'xpath=>//*[@id="btn_editVersion"]'
        self.click(version_mod_link)

    # 点击删除版本
    def version_del_click(self):
        version_del_link = 'xpath=>//*[@id="btn_delVersion"]'
        self.click(version_del_link)

    # 点击版本升级 点击之后跳转到DrcVerMgrUpdatePage页面
    def version_update_click(self):
        version_qry_link = 'xpath=>//*[@id="btn_drcVersionUpdate"]'
        self.click(version_qry_link)

    # 选择drc版本 推荐方法 先填入版本名称，点击查询，然后选定 可选参数version_id主要用于校验 可以不填写
    def choose_drc_version(self, version_name, version_id='0'):
        self.input_drc_version_name(version_name)
        self.qry_version_click()
        return self.version_id_select_click_single(version_id)

    # 填写保存ftp版本信息弹窗
    def set_ftp_info(self, dict_ftp):
        self.version_ftp_qry_click()
        if not self.is_prompt_visible_ftp():
            self.info()
            self.get_windows_img()
            logger.error('没有弹出版本ftp信息弹窗')
            return False
        self.input_ftp_domain_name(dict_ftp['ftp域名'])
        self.input_ftp_port(dict_ftp['ftp端口'])
        self.input_ftp_user(dict_ftp['ftp用户名'])
        self.input_ftp_password(dict_ftp['ftp密码'])
        self.save_cfg_click()
        assert (self.info())
        if self.info_text() == dict_ftp['预期结果']:
            logger.info('版本入库结果符合预期：%s', dict_ftp['预期结果'])
            self.enter_click()
            return True
        else:
            logger.error('版本入库结果不符合预期 预期结果：%s,实际结果:%s' % (dict_ftp['预期结果'], self.info_text()))
            self.esc_click()
            return False

    # 填写新增/修改drc版本入库弹窗
    def add_or_mod_drc_version(self, dict_version):
        if dict_version['DRC版本名称']:
            self.input_version_name(dict_version['DRC版本名称'])
        if dict_version['上传者']:
            self.input_version_author(dict_version['上传者'])
        if dict_version['上传时间']:
            self.input_version_time(dict_version['上传时间'])
        if dict_version['版本所在路径']:
            self.input_version_path(dict_version['版本所在路径'])
        self.version_upload_click()
        self.sleep(1)  # 必须增加sleep，否则一次性增加两个相同版本
        if self.info_text() == dict_version['预期结果']:
            logger.info('版本入库结果与预期一致：%s' % dict_version['预期结果'])
            self.enter_click()
            return True
        else:
            self.get_windows_img()
            logger.error('版本入库结果与预期不一致，预期结果：%s，实际结果：%s' % (dict_version['预期结果'], self.info_text()))
            return False

    # 新增drc版本
    def add_drc_version(self, dict_version):
        self.version_add_click()
        if not self.is_prompt_visible_add():
            self.info()
            self.get_windows_img()
            return False
        return self.add_or_mod_drc_version(dict_version)

    # 修改drc版本
    def mod_drc_version(self, dict_version):
        if not self.version_id_select_click(dict_version['版本记录编号']):
            return False
        self.version_mod_click()
        if not self.is_prompt_visible_add():
            self.info()
            self.get_windows_img()
            return False
        return self.add_or_mod_drc_version(dict_version)

    # 删除drc版本
    def del_drc_version(self):
        self.version_del_click()
        assert (self.info())
        if self.info_text() == '确定 删除选定版本':
            self.enter_click()
            self.esc_click()
            self.sleep(1)
            assert (self.info())
            if self.info_text() == '任务删除成功':
                self.esc_click()
                logger.info('drc版本删除成功')
                return True
        else:
            self.get_windows_img()
            logger.error('drc版本删除失败%s' % (self.info_text()))
            self.esc_click()
            return False
