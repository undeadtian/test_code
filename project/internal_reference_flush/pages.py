import os
import time
from selenium.common.exceptions import NoSuchElementException
import os.path
import configparser
from common.Log import Logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from common.Log import Logger

logger = Logger('reference_flush').getlog()

class BasePage(object):
    """
    定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法到这个类
    """

    def __init__(self, driver):
        self.driver = driver

    # quit browser and end testing
    def quit_browser(self):
        self.driver.quit()

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()
        logger.debug("Click forward on current page.")

    # 浏览器后退操作
    def back(self):
        self.driver.back()
        logger.debug("Click back on current page.")

    # 隐式等待 最好别用
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logger.debug("wait for %d seconds." % seconds)

    # 点击关闭当前窗口
    def close(self):
        try:
            self.driver.close()
            logger.debug("Closing and quit the browser.")
        except NameError as e:
            logger.error("Failed to quit the browser with %s" % e)

    # 保存图片
    def get_windows_img(self):
        """
        在这里我们把file_path这个参数写死，直接保存到我们项目根目录的一个文件夹.\Screenshots下
        """
        file_path = os.path.dirname(os.path.abspath('.')) + '/screenshots/'
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.debug("Had take screenshot and save to folder : /screenshots")
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.get_windows_img()

    # 定位元素方法
    def find_element(self, selector):
        """
         这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         submit_btn = "id=>su"
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
        :param selector:
        :return: element
        """
        element = ''
        # print(selector)
        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]
        # print(selector_by)
        # print(selector_value)
        if selector_by == "i" or selector_by == 'id':
            try:
                element = self.driver.find_element_by_id(selector_value)
                logger.debug("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                self.get_windows_img()  # take screenshot
        elif selector_by == "n" or selector_by == 'name':
            element = self.driver.find_element_by_name(selector_value)
        elif selector_by == "c" or selector_by == 'class_name':
            element = self.driver.find_element_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            element = self.driver.find_element_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            try:
                element = self.driver.find_element_by_xpath(selector_value)
                logger.debug("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                self.get_windows_img()
                raise ValueError("NoSuchElementException.")
        elif selector_by == "s" or selector_by == 'selector_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return element

    # 输入
    def type(self, selector, text):

        el = self.find_element(selector)
        el.clear()
        try:
            el.send_keys(text)
            logger.debug("Had type \' %s \' in inputBox" % text)
        except NameError as e:
            logger.error("Failed to type in input box with %s" % e)
            self.get_windows_img()

    # 清除文本框
    def clear(self, selector):

        el = self.find_element(selector)
        try:
            el.clear()
            logger.debug("Clear text in input box before typing.")
        except NameError as e:
            logger.error("Failed to clear in input box with %s" % e)
            self.get_windows_img()

    # 点击元素
    def click(self, selector):
        el = self.find_element(selector)
        try:
            el.click()
            logger.debug("The element was clicked.")
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

    # 点击元素
    def click1(self, selector):
        el = self.find_element(selector)
        try:
            el.send_keys(Keys.ENTER)
            logger.debug("The element was clicked.")
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

    # 或者网页标题
    def get_page_title(self):
        logger.debug("Current page title is %s" % self.driver.title)
        return self.driver.title

    # 获取当前句柄
    def get_handle(self):
        logger.debug("当前的句柄是：%s" % self.driver.current_window_handle)
        return self.driver.current_window_handle

    # 切换句柄
    def sent_handle(self):
        # 获取所有的句柄
        all_h = self.driver.window_handles
        # 获取当前句柄
        h = self.driver.current_window_handle
        # 循环判断是否与首句柄相同
        for i in all_h:
            if i != h:  # 如果不等于首句柄则切换
                logger.debug("切换句柄")
                self.driver.switch_to_window(i)

    # 获取当前页面url
    def get_curr_url(self):
        logger.debug("当前页面的url是：%s " % self.driver.current_url)
        return self.driver.current_url

    # 复选框的勾选
    def checkboxes(self, selector):
        el = self.find_element(selector)
        try:
            for checkbox in el:
                checkbox.click()
                time.sleep(1)
            logger.debug("复选框勾选成功")
        except Exception as e:
            logger("勾选失败的原因% s" % e)

    def selected(self, selector):
        try:
            if self.find_element(selector).is_selected():
                logger.debug("该元素已经被勾选")
                return True
            else:
                logger.debug("该元素已经被勾选")
                return False
        except Exception as e:
            logger.debug("error：", format(e))
            return False

    def info(self):
        try:
            info = self.find_element('class_name=>idlg-main')
            logger.debug("弹出提示：\' %s \'" % info.text)
            return True
        except Exception as e:
            logger.debug("未弹出提示%s" % format(e))
            return False

    def info_text(self):
        info = self.find_element('class_name=>idlg-main')
        return info.text

    def esc_click(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def enter_click(self):
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    def is_visible(self, selector):
        try:
            ui.WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, selector)))
            return True
        except Exception as e:
            logger.error(format(e))
            return False

    def is_visible1(self, selector):
        try:
            ui.WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, selector)))
            return True
        except Exception as e:
            logger.error(format(e))
            return False

    def is_not_visible(self, selector):
        try:
            ui.WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located(By.XPATH, selector))
            return True
        except TimeoutError:
            return False

    def get_id_attribute(self, selector):
        try:
            att_id = self.find_element(selector).get_attribute('id')
            logger.debug("Get attribute id %s successed." % att_id)
            return att_id
        except:
            logger.error("Get attribute id failed")
            return ''

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)
        logger.debug("Sleep for %d seconds" % seconds)

class LoginHomePage(BasePage):
    """
    登录confluence
    """
    config = configparser.ConfigParser()
    file_path = os.path.join(os.path.join(os.path.abspath('.'), 'config'), 'config.ini')
    config.read(file_path)
    username = config.get("user", "username")
    password = config.get("user", "password")
    user_link = 'xpath=>//*[@id="os_username"]'
    pass_link = 'xpath=>//*[@id="os_password"]'
    login_link = 'xpath=>//*[@id="loginButton"]'

    # user_link = "c => loginuser"
    # pass_link = "c => loginpwd"

    def set_username(self):
        admin_user = self.find_element(self.user_link)
        admin_user.send_keys(self.username)
        self.wait(0.1)

    def set_password(self):
        admin_pass = self.find_element(self.pass_link)
        admin_pass.send_keys(self.password)
        self.wait(0.1)

    def click_login(self):
        self.click(self.login_link)
        self.sleep(3)

    def is_login_sucess(self):
        return self.is_visible('//*[@id="msg"]')
    # //*[@id="msg"]

class ReferencePage(BasePage):
    """
    登录confluence
    """
    def __init__(self, driver):
        BasePage.__init__(self,driver)
        self.index = 0

    def get_index(self, camera_no):
        if self.index:
            return self.index
        try:
            index = 1
            while True:
                link = 'xpath=>//*[@id="table-joiner-1606908769696_1839827944"]/div[1]/div/table/tbody/tr[{}]/td[5]'.format(
                    index)
                if self.find_element(link).text == str(camera_no):
                    logger.error('confluence相机编号为：{}的记录在第{}条'.format(camera_no,index))
                    self.index = index
                    return index
                index += 1
        except:
            logger.error('confluence页面中找不到相机编号为：{}的记录'.format(camera_no))
            return 0

    def get_sn_no(self):
        if not self.index:
            return 0
        link = 'xpath=>//*[@id="table-joiner-1606908769696_1839827944"]/div[1]/div/table/tbody/tr[{}]/td[4]'.format(
                    self.index)
        try:
            sn_no = self.find_element(link).text
            logger.debug('获取对应camera对应sn号：{}'.format(sn_no))
            return sn_no
        except:
            logger.error('获取sn号失败')
            return 0

    def download_json(self):
        if not self.index:
            return 0
        link = 'xpath=>//*[@id="table-joiner-1606908769696_1839827944"]/div[1]/div/table/tbody/tr[{}]/td[9]/a'.format(
                    self.index)
        try:
            self.click(link)
            time.sleep(5)
        except:
            logger.error('获取json文件失败')