import paramiko
import sys
from paramiko_expect import SSHClientInteraction
# import prompt

host = '172.18.13.111'
port = 22
username = 'broadxt'
password = 'broadxt333'

# 自行修改输出函数
json_list = []


def output_func(msg):
    print(msg)
    sys.stdout.write(msg)
    json_list.append(msg)
    sys.stdout.flush()


def conn_tail():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        client.connect(host, port, username, password)
        interact = SSHClientInteraction(client, timeout=10)

        interact.expect(prompt)
        command = 'tail -f /dr/drsu_16388/DR_APP/log.txt | grep -aE "ulAidataNO|ai_recv"'
        interact.send(command)
        # log_name = path.split('/')[-1].split('.')[0]
        # interact.tail(line_prefix=log_name + ': ',output_callback=output_func)
        interact.tail(output_callback=output_func)
    except:
        raise

if __name__ == '__main__':
    conn_tail()
    print(json_list)