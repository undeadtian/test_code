# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : script.py
@Author  : 王白熊
@Data    ： 2020/12/16 11:19
"""
import configparser
import re
import os
import json
import time
import paramiko
from argparse import ArgumentParser
from shutil import copyfile
from common.Log import Logger
from ssh.base_command import BaseCommand
from project.internal_reference_flush.web_script import get_reference_info
import logging

RET_FILE_ERROR = 10
RET_DOWN_LOAD_ERROR = 20
RET_SUCCESS = 0
RET_JSON_DATA_ERROR = 30
config = configparser.ConfigParser()
file_path = os.path.join(os.path.join(os.path.abspath('.'), 'config'), 'config.ini')
config.read(file_path)
logger = Logger('reference_flush').getlog()


class SSHConnection(BaseCommand):
    def __init__(self, senior_no, host=None, port=None, username=None, password=None, ):
        BaseCommand.__init__(self, host, port, username, password)
        self.senior_no = senior_no
        self.sn_no = 0
        logger.info('建立ssh连接，主机：%s，端口：%s, 账号：%s， 密码：%s'
                    % (self._host, self._port, self._username, self._password))
        self._connect()  # 建立连接

    def get_remote_file(self):
        command = 'ls /home/broadxt/camera_toolbox/{} | grep json'.format(self.senior_no)
        remote_file = self.exec_command_retstr(command)
        print(remote_file)
        return remote_file

    def download_special_file(self, ):
        remote_file = self.get_remote_file()
        if not remote_file:
            logger.error('找不到指定传感器编号的内参json文件')
            return RET_FILE_ERROR
        elif len(remote_file.split()) > 1:
            logger.error('找不到指定传感器编号的内参文件夹中有多个json文件')
            return RET_FILE_ERROR
        remote_dir = '/home/broadxt/camera_toolbox/{}/{}'.format(self.senior_no, remote_file).strip()
        dir_path = os.path.join(os.path.abspath('.'), 'json')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        json_path = os.path.join(dir_path, '{}.json'.format(self.senior_no))
        if os.path.exists(json_path):
            os.remove(json_path)
        self.download(remote_dir, json_path)
        return RET_SUCCESS

    def get_json_file_size(self):
        json_file = r'json\{}.json'.format(self.senior_no)
        size = os.path.getsize(json_file)
        return size

    def get_txt_file_size(self):
        txt_file = r'json\{}.txt'.format(self.senior_no)
        size = os.path.getsize(txt_file)
        return size

    def check_json_file(self):
        json_file = r'json\{}.json'.format(self.senior_no)
        if not os.path.isfile(json_file):
            logger.error('文件下载失败')
            return None
        with open(json_file) as fp:
            data_str = fp.read()
            data_list = json.loads(data_str)
            if data_list['fx'] < 5000 and data_list['fy'] < 5000:
                if data_list['segma_fx']['std(%)'] > 1 or \
                        data_list['segma_fy']['std(%)'] > 1 or \
                        data_list['segma_cx']['std(%)'] > 1 or \
                        data_list['segma_cy']['std(%)'] > 1:
                    logger.error(
                        '序号{}内参数据异常'.format(self.senior_no))
                    # return None
            elif data_list['fx'] > 7000 and data_list['fy'] > 7000:
                if data_list['segma_fx']['std(%)'] > 1 or \
                        data_list['segma_fy']['std(%)'] > 1:
                    logger.error(
                        '序号{}内参数据异常'.format(self.senior_no))
                    # return None
                elif data_list['segma_cx']['std(%)'] > 1 or \
                        data_list['segma_cy']['std(%)'] > 1:
                    logger.warning('序号{}内参数据异常'.format(self.senior_no))
                    # return None
        return data_list

    def json_to_txt(self):
        data_list = self.check_json_file()
        txt_file = r'json\{}.txt'.format(self.senior_no)
        demo_file = r'json\demo.txt'
        if os.path.exists(txt_file):
            os.remove(txt_file)
        with open(txt_file, 'a+', encoding='utf-8') as fp, open(demo_file, encoding='utf-8') as demo:
            line = demo.readline()
            while line:
                print(line)
                pattern = re.compile(r'([a-z]+[0-9]+)[:]\s[-]?([0-9]+\.[0-9]+)')
                line_data = pattern.search(line)
                if line_data:
                    write_line = '  {}: {}\n'.format(line_data.groups()[0],
                                                     str(data_list[line_data.groups()[0]]).strip())
                else:
                    line_data = re.compile(r'[SN][:]\s([0-9]+)').search(line)
                    if line_data:
                        write_line = 'SN: {}'.format(self.sn_no)
                    else:
                        write_line = line
                fp.write(write_line)
                line = demo.readline()
            # fp.write()


class SSHConnectionARM(BaseCommand):
    def __init__(self, senior_no, host=None, port=None, username=None, password=None, ):
        BaseCommand.__init__(self, host, port, username, password)
        self.senior_no = senior_no
        self.sn_no = 0
        logger.info('建立ssh连接，主机：%s，端口：%s, 账号：%s， 密码：%s'
                    % (self._host, self._port, self._username, self._password))
        self._connect()  # 建立连接

    def put_special_file(self, ):
        remote_dir = '/share/camera_flash_isp_user/{}.txt'.format(self.senior_no)
        dir_path = os.path.join(os.path.abspath('.'), 'json')
        txt_path = os.path.join(dir_path, '{}.txt'.format(self.senior_no))
        self.put(txt_path, remote_dir)

    def get_remote_file(self):
        command = "ls /share/camera_flash_isp_user | grep -E 'read_tmp|write_tmp'"
        remote_file = self.exec_command_retstr(command).split()
        print(remote_file)
        return remote_file

    def download_special_file(self, ):
        remote_file = self.get_remote_file()
        if len(remote_file) != 2:
            logger.error('无法读取写文件和读文件记录')
            return RET_FILE_ERROR
        dir_path = [os.path.join('data', 'read_tmp_{}.txt'.format(self.senior_no)),
                    os.path.join('data', 'write_tmp_{}.txt'.format(self.senior_no))]
        self.download(os.path.join('/share/camera_flash_isp_user/', remote_file[0]), dir_path[0])
        self.download(os.path.join('/share/camera_flash_isp_user/', remote_file[1]), dir_path[1])
        self.del_file(os.path.join('/share/camera_flash_isp_user/', remote_file[0]))
        self.del_file(os.path.join('/share/camera_flash_isp_user/', remote_file[1]))
        return RET_SUCCESS

    def check_txt_file(self, file_size):
        command = ''.join(['du -b /share/camera_flash_isp_user/{}.txt'.format(self.senior_no), " | awk '{print $1}'"])
        file_size_ = self.exec_command_retstr(command)
        # print(file_size_)
        if not file_size or int(file_size_) != file_size:
            return False
        else:
            return True

    def int_ref_flush(self):
        # command = 'cd /share/camera_flash_isp_user; ./write v1 {}.txt > tmp.txt'.format(self.senior_no)
        # command = 'cd /share/camera_flash_isp_user; pwd'.format(self.senior_no)
        command1 = 'cd /share/camera_flash_isp_user'
        command2 = './write v1 {}.txt > write_tmp.txt'.format(self.senior_no)
        self.send_command(command1)
        self.send_command(command2)

    def int_ref_read(self):
        command1 = 'cd /share/camera_flash_isp_user'
        command2 = './read v1 > read_tmp.txt'.format(self.senior_no)
        self.send_command(command1)
        self.send_command(command2)

    def check_flush(self):
        write_file = 'write_tmp.txt'
        read_file = 'read_tmp.txt'
        txt_file = r'json\{}.txt'.format(self.senior_no)
        fp1 = open(write_file, 'rb')
        fp2 = open(read_file, 'rb')
        fp3 = open(txt_file, 'rb')
        st1 = os.stat(write_file)
        st2 = os.stat(read_file)
        st3 = os.stat(txt_file)
        # print(st1.st_size, st2.st_size, st3.st_size)
        if (st1.st_size - 116) != st3.st_size or (st2.st_size - 70) != st3.st_size:
            return False
        fp1.seek(113, 0)
        fp2.seek(68, 0)
        index = 0
        for i in range(st3.st_size + 1):
            b1 = fp1.read(1)
            b2 = fp2.read(1)
            b3 = fp3.read(1)
            # print(index,b1,b2,b3)
            index += 1
            if not b3:
                logger.info('内参文件写入成功')
                return True
            if b1 != b2 or b2 != b3:
                logger.error('read出的数据与期望数据不一致')
                return False

class FileParse(object):
    def __init__(self, senior_no):
        self.senior_no = senior_no
        self.sn_no = get_reference_info(senior_no)
        self.cp_json_file()

    def cp_json_file(self):
        source_file = os.path.join(r'C:\Users\Admin\Downloads', '{}.json'.format(self.senior_no))
        destination_file = r'json\{}.json'.format(self.senior_no)
        if not os.path.isfile(source_file):
            logger.error('未找到下载的json文件')
            return
        copyfile(source_file, destination_file)

    def get_json_file_size(self):
        json_file = r'json\{}.json'.format(self.senior_no)
        size = os.path.getsize(json_file)
        return size

    def get_txt_file_size(self):
        txt_file = r'json\{}.txt'.format(self.senior_no)
        size = os.path.getsize(txt_file)
        return size

    def check_json_file(self):
        json_file = r'json\{}.json'.format(self.senior_no)
        if not os.path.isfile(json_file):
            logger.error('json文件复制失败')
            return None
        with open(json_file) as fp:
            data_str = fp.read()
            data_list = json.loads(data_str)
            if data_list['fx'] < 5000 and data_list['fy'] < 5000:
                if data_list['segma_fx']['std(%)'] > 1 or \
                        data_list['segma_fy']['std(%)'] > 1 or \
                        data_list['segma_cx']['std(%)'] > 1 or \
                        data_list['segma_cy']['std(%)'] > 1:
                    logger.error(
                        '序号{}内参数据异常'.format(self.senior_no))
                    # return None
            elif data_list['fx'] > 7000 and data_list['fy'] > 7000:
                if data_list['segma_fx']['std(%)'] > 1 or \
                        data_list['segma_fy']['std(%)'] > 1:
                    logger.error(
                        '序号{}内参数据异常'.format(self.senior_no))
                    # return None
                elif data_list['segma_cx']['std(%)'] > 1 or \
                        data_list['segma_cy']['std(%)'] > 1:
                    logger.warning('序号{}内参数据异常'.format(self.senior_no))
                    # return None
        return data_list

    def json_to_txt(self):
        data_list = self.check_json_file()
        txt_file = r'json\{}.txt'.format(self.senior_no)
        demo_file = r'json\demo.txt'
        if os.path.exists(txt_file):
            os.remove(txt_file)
        with open(txt_file, 'a+', encoding='utf-8') as fp, open(demo_file, encoding='utf-8') as demo:
            line = demo.readline()
            while line:
                print(line)
                pattern = re.compile(r'([a-z]+[0-9]+)[:]\s[-]?([0-9]+\.[0-9]+)')
                line_data = pattern.search(line)
                if line_data:
                    write_line = '  {}: {}\n'.format(line_data.groups()[0],
                                                     str(data_list[line_data.groups()[0]]).strip())
                else:
                    line_data = re.compile(r'[SN][:]\s([0-9]+)').search(line)
                    if line_data:
                        write_line = 'SN: {}'.format(self.sn_no)
                    else:
                        write_line = line
                fp.write(write_line)
                line = demo.readline()
            # fp.write()
#
# def reference_flush_single(senior_no, arr_x86, arr_arm):
#     arr_x86[0:0] = [senior_no]
#     arr_arm[0:0] = [senior_no]
#     A = SSHConnection(*arr_x86)
#     B = SSHConnectionARM(*arr_arm)
#     if A.download_special_file() != RET_SUCCESS:
#         exit(-1)
#     A.json_to_txt()
#     txt_size = A.get_txt_file_size()
#     B.put_special_file()
#     B.check_txt_file(txt_size)
#     B.int_ref_flush()
#     B.int_ref_read()
#     B.get_remote_file()
#     B.download_special_file()
#     ret = B.check_flush()
#     A.close()
#     B.close()

def reference_flush_single(senior_no, arr_arm):

    arr_arm[0:0] = [senior_no]
    A = FileParse(senior_no)
    A.json_to_txt()
    txt_size = A.get_txt_file_size()
    B = SSHConnectionARM(*arr_arm)
    B.put_special_file()
    B.check_txt_file(txt_size)
    B.int_ref_flush()
    B.int_ref_read()
    B.get_remote_file()
    B.download_special_file()
    ret = B.check_flush()
    B.close()
    return ret

def get_x86_config(item):
    try:
        return config.get('X86', item)
    except:
        logger.warning('没有在配置文件中找到X86的%s元素' % item)
        return None


def get_arm_config(item):
    try:
        return config.get('ARM', item)
    except:
        logger.warning('没有在配置文件中找到ARM的%s元素' % item)
        return None


def reference_flush(senior_no):
    # arg_parser = ArgumentParser()
    # arg_parser.add_argument('senior_no', help='')
    # args = arg_parser.parse_args()
    arr_arm = [get_arm_config('host'), int(get_arm_config('port')),
               get_arm_config('username'), get_arm_config('password')]
    for i in senior_no:
        reference_flush_single(i, arr_arm)


if __name__ == '__main__':
    senior_no = [606]
    reference_flush(senior_no)
