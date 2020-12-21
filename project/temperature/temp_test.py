# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : temp_test.py
@Author  : 王白熊
@Data    ： 2020/12/4 10:18
"""
from ssh.drsu_ssh import DrsuSSHConnection
from common.Log import Logger
import time
import re
import xlwt
import threading
from xlwt import Font, XFStyle

logger = Logger('temperature').getlog()


senior_name = ['camera0', 'camera1', 'radar', 'ai_out']
lock = threading.Lock()


class DrsuSSHConnectionTemp(DrsuSSHConnection):
    # b'20201204 11:19:02.391790[607826]_AI_DATA0:INF:L0180:ai_data_notify_cameradp_msg:ai notify cameradp msg, \x1b[01;31m\x1b[KulAidataNO(0)\x1b[m\x1b[K, CameraFrameCount(43201)\r'
    # 20201204 11:19:02.391790[607826]_AI_DATA0:INF
    # [:8]
    # [9:17]
    # [18: 24]
    # 保证不会出现多个线程对同一个地方写，所以就不加线程锁了
    def __init__(self, drsu_id, is_sim, drc_id, encode='utf-8'):
        DrsuSSHConnection.__init__(self, drsu_id=drsu_id, is_sim=is_sim, drc_id=drc_id, )
        self.fp = None
        self.sheet1 = None
        self.encoding = encode
        self.rq = time.strftime('%Y%m%d', time.localtime(time.time()))

    def get_xlwt_handle(self):
        self.fp = xlwt.Workbook()
        self.sheet1 = self.fp.add_sheet(u'sheet1', cell_overwrite_ok=True)
        self.sheet1.write(0, 0, 'camera0')
        self.sheet1.write(0, 2, 'camera1')
        self.sheet1.write(0, 4, 'radar')
        self.sheet1.write(0, 6, 'ai_out')
        self.sheet1.write(0, 8, 'cpu_tmp')
        self.sheet1.write(0, 9, 'gpu_tmp')

    def write_xl(self, index, col, value, style=None):
        if not self.fp:
            self.get_xlwt_handle()
        # lock.acquire()
        if style:
            self.sheet1.write(index, col, value, style=style)
        else:
            self.sheet1.write(index, col, value)
        self.fp.save(self.rq + 'temp.xls')
        # lock.release()

    def check_type(self, line):
        pattern = re.compile(r'ulAidataNO')
        pattern1 = re.compile(r'[(]0[)]')
        pattern2 = re.compile(r'[(]1[)]')
        pattern3 = re.compile(r'[(]6[)]')
        pattern4 = re.compile(r'ai_recv')
        if pattern.search(line):
            if pattern1.search(line):
                return 0
            elif pattern2.search(line):
                return 1
            elif pattern3.search(line):
                return 2
            else:
                return 10
        elif pattern4.search(line):
            return 3
        else:
            return 10

    def get_report_info_perid(self, cmd, diff_time, thre_time, max_number, ):
        # 发送要执行的命令
        pre_time_stamp = [0] * 4
        self._channel.send(cmd + '\r')
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        time_stamp_arr = []
        index = [0] * 4
        current_line = b''
        line_counter = 0
        line_feed_byte = '\n'.encode(self.encoding)
        while True:
            style = None
            buffer = self._channel.recv(1)
            if len(buffer) == 0:
                logger.info('end______________')
                return
            current_line += buffer
            if buffer == line_feed_byte:
                line = current_line.decode(self.encoding)
                # logger.debug('shell显示：%s' % line)
                col = self.check_type(line)
                if not line.startswith(self.rq) or col == 10:
                    line_counter += 1
                    current_line = b''
                    continue
                time_stamp = int(time.mktime(time.strptime(' '.join([line[:8], line[9:17]]), "%Y%m%d %H:%M:%S")))
                time_stamp_dec = line[18: 21]  # 精确到毫秒
                time_stamp = time_stamp * 1000 + int(time_stamp_dec)
                logger.info('%s:%s' % (senior_name[col], time_stamp))
                if pre_time_stamp[col] == 0:
                    pre_time_stamp[col] = time_stamp
                else:
                    if abs((time_stamp - pre_time_stamp[col]) - diff_time[col]) > thre_time[col]:
                        logger.error(
                            '两帧数据间隔为{}ms,时间戳分别为:({},{}),行号：{}'.format(time_stamp - pre_time_stamp[col], time_stamp,
                                                                      pre_time_stamp[col],
                                                                      index[col]))
                        style = XFStyle()
                        fnt = Font()
                        fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑  
                        fnt.colour_index = 2  # 设置其字体颜色  
                        fnt.bold = True
                        style.font = fnt
                self.write_xl(index[col] + 1, col*2, time_stamp)
                self.write_xl(index[col] + 1, col*2 + 1, time_stamp - pre_time_stamp[col], style=style)
                index[col] += 1
                pre_time_stamp[col] = time_stamp
                line_counter += 1
                current_line = b''

    def get_temp_info(self, col, max_number):
        index = 0
        cpu_arr, gpu_arr = [], []
        while True:
            cpu_temp, gpu_temp = self.get_cpu_gpu_temp()
            logger.info('cpu_temp:%s, gpu_temp:%s' % (cpu_temp, gpu_temp))
            cpu_arr.append(cpu_temp)
            gpu_arr.append(gpu_temp)
            self.write_xl(index + 1, col, cpu_temp)
            self.write_xl(index + 1, col + 1, gpu_temp)
            time.sleep(60)
            index += 1
            if max_number == index:
                break
        return cpu_arr, gpu_arr


def temperature_test(drsu_id):
    drsuconn = DrsuSSHConnectionTemp(str(drsu_id), is_sim=False, drc_id=None)
    # drsuconn.get_xlwt_handle()
    # drsuconn.send_command_temp('tail -f /dr/drsu_16388/DR_APP/log.txt | grep -a "ulAidataNO(0)"', 60000, 50, 1000, 0)
    if drsuconn.remote_ps_drsu_process_num() != 0:
        # 如果drsu已经启动不重新启动
        logger.info('drsu已启动')

    else:
        drsuconn.remote_start_drsu()
        time.sleep(100)
        if not drsuconn.is_drsu_ready():
            logger.error('drsu启动不成功')
    command = 'tail -F /dr/drsu_16388/DR_APP/log.txt >&2'
    time_diff = [60000, 60000, 44000, 60000]
    time_dev = [50, 50, 1000,  50]
    max_number = 1000
    t1 = threading.Thread(target=drsuconn.get_report_info_perid, name='senior',
                          args=(command, time_diff, time_dev, max_number))
    t2 = threading.Thread(target=drsuconn.get_temp_info, name='temp',
                          args=(8, max_number))

    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    temperature_test(54321)
