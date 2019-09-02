# coding:utf-8

import time
import re
from slackclient import SlackClient
import sys
import math
import serial
import numpy as np
import statistics
import socket

def main():
    '''
    UDP通信サーバーのセッティング
    受信データの解析
    解析結果をslack botで送信を行う
    '''

    token = "トークン" # メモしておいたトークンを設定
    sc = SlackClient(token)

    print("bot boot")

    channels_name = "bot_name"

    test = 0

    n = 40

    time_window = 100

    window_list_xyz = []
    time_data = []

    amount = 250

    Decrease_point = [0,0]

    ave_xyz = 0

    udp_data_xyz = 0

    median = 0

    index = 1


    '''
    UDP通信サーバーのセッティング
    '''
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except s(ocket.error, msg) :
        print ('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    try:
        s.bind(('', 3333))
    except (socket.error , msg):
        print ('Bind failed. Error: ' + str(msg[0]) + ': ' + msg[1])
        sys.exit()

    print ('Server listening')

    if sc.rtm_connect():
        while True:
            udp_recv = s.recvfrom(1024)
            udp_data = udp_recv[0].strip()
            udp_data = re.findall(r'[0-9]+', str(udp_data))

            udp_data_xyz = int(udp_data[0])

            window_list_xyz.append(udp_data_xyz)
            time_data.append(udp_data_xyz)

            slack_data = sc.rtm_read()
            test = test + 1

            if len(window_list_xyz) > n:
                window_list_xyz.pop(0)

            if  len(window_list_xyz) == n:
                ''''
                畳み込み積分を行う
                ''''
                ave_xyz = np.convolve(np.array(window_list_xyz, dtype='int64'), np.ones(n)/float(n), 'valid')

            if len(time_data) > time_window:
                time_data.pop(0)

            if len(time_data) == time_window:
                '''
                最頻値を取得
                '''
                median = statistics.median(time_data)
                time_data.pop(0)

            if  len(window_list_xyz) == n:

                if median-ave_xyz > 50 and index - Decrease_point[0] > 50:
                    print("push")
                    print(index - Decrease_point[0])
                    print(median-ave_xyz)
                    Decrease_point[0] = index
                    Decrease_point[1] = Decrease_point[1] + 1

            if len(slack_data) > 0:
                for item in slack_data:
                    message_check = create_message(item)
                    if message_check is True:
                        amount_answer = math.floor(((amount-Decrease_point[1]*5)/amount)*100)
                        print(amount_answer)
                        messagetext = "シャンプーの残りの量は"+str(amount_answer)+"%です"
                        sc.rtm_send_message(item['channel'], messagetext)
                        sc.api_call('files.upload', channels=item['channel'], as_user=True, filename='./image_data/'+str(amount_answer)+'.png', file=open('./image_data/'+str(amount_answer)+'.png', 'rb'))

            index = index + 1
        s.close()
    else:
        print("Connection Failed, invalid token?")


def create_message(data):
    '''
    slackからbotへ送信されたメッセージ内に量が含まれているかを調べる
    '''

    if "type" in data.keys():

        if data["type"] == "message":

            if re.search(u"(.*量.*)", data["text"]) is not None:
                return True

    return None


if __name__=="__main__":
    main()
    sys.exit()
