# -*-coding:utf-8-*-
import requests
import urllib3
import os
from PIL import Image
import re
from Info import *
from Config import *
import time
import json
import random
import sys

urllib3.disable_warnings()
session = requests.session()
session.headers = HEADERS
session.verify = False


def get_image():
    i = 5
    while i:
        try:
            response = session.get(URLINFO['captcha-image']['url'].format(random.random))
            # print(session.cookies)
            with open('img.jpg', 'wb') as f:
                f.write(response.content)
            im = Image.open('img.jpg')
            im.show()
            # 关闭代码，实际图片浏览器没有关闭
            im.close()
            break
        except Exception as e:
            print(e)
            time.sleep(2)
            i -= 1
    print('-------------------------')
    print('|  1  |  2  |  3  |  4  |')
    print('|     |     |     |     |')
    print('-------------------------')
    print('|  5  |  6  |  7  |  8  |')
    print('|     |     |     |     |')
    print('-------------------------')
    code = input('请输入验证码（如123）：')
    code_all = [
        '30,45',
        '105,45',
        '178,45',
        '255,45',
        '31,120',
        '114,120',
        '180,120',
        '255,120'
    ]
    ans = []
    for num in code:
        ans.append(code_all[int(num) - 1])
    answer = ','.join(ans)
    return answer


def check_image():
    data = {
        'answer': get_image(),
        'login_site': 'E',
        'rand': 'sjrand'
    }
    response = session.post(URLINFO['captcha-check']['url'], data=data)
    # print(session.cookies)
    if response.json()['result_code'] == '4':
        print('验证码通过')
        return True
    else:
        print('验证码失败，请重试')
        return False


def login_first():
    print('第一步登陆验证中...')
    data = {
        'username': USER_NAME,
        'password': PASSWORD,
        'appid': 'otn',
    }
    response = session.post(URLINFO['login']['url'], data=data).json()
    if response['result_code']:
        print('第一步登陆验证失败')
        return False
    print('第一步登陆验证成功')
    session.post(URLINFO['userLogin']['url'], data={'_json_att': ''})

    return True


# 访问uamtk 获取 newapptk
def login_second():
    print('第二步登陆验证中...')
    response = session.post(URLINFO['uamtk']['url'],
                            data={'appid': 'otn'},
                            headers=URLINFO['uamtk']['headers']).json()
    if response['result_code']:
        print('第二步登陆验证失败')
        return False
    print('第二步登陆验证成功')
    return response['newapptk']


# 登陆最后一步，访问 uamauthclient
def login_third(newapptk):
    print('第三步登陆验证中...')
    i = 5
    while i:
        try:
            response = session.post(URLINFO['uamauthclient']['url'],
                                data={'tk': newapptk}, timeout=5).json()
            if response['result_code'] == 0:
                # print('登录用户: ' + response['username'])
                return True
        except json.decoder.JSONDecodeError:
            i -= 1
        finally:
            time.sleep(1)
    print('登陆失败')
    return False


def login():
    session.get(URLINFO['init']['url'])
    if not check_image():
        return False
    print('用户登陆中...')
    if not login_first():
        return False
    newapptd = login_second()
    # print(newapptd)
    if login_third(newapptd):
        print('登陆成功')
        return True
    return False


def get_city_code():
    city_code = requests.get(URLS['city_code'], verify=False).text
    with open('city_code.txt', 'w') as f:
        f.write(city_code)


def trans_city_code(uchar):
    if not os.path.exists('city_code.txt'):
        get_city_code()
    with open('city_code.txt', 'r') as f:
        city_code = f.readline()

    if u'\u9fa5' >= uchar[0] >= u'\u4e00':  # 中文
        return re.compile(uchar+'\|(.+?)\|').findall(city_code)[0]
    else:
        return re.compile('\|([\u4E00-\u9FA5)]+?)\|'+uchar).findall(city_code)[0]


def check_no(s):
    if s == '':
        s = '-'
    return s


def print_train_info(train_list):
        # secretStr：0
        # 内容 预定:1
        # 车次：3
        # 起始站：4
        # 终点站：5
        # 出发站：6
        # 到达站：7
        # 出发时间：8
        # 达到时间：9
        # 历时：10
        # 是否可以预订（Y可以 N不可以）:   11
        # 商务特等座：32
        # 一等座：31
        # 二等座：30
        # 高级软卧：21
        # 软卧：23
        # 动卧：33
        # 硬卧：28
        # 软座：24
        # 硬座：29
        # 无座：26
        # 其他：22
        # 车票出发日期：13
    if train_list:
        print('车次  出发站 到站 出发时间 到站时间 历时 特等 一等 二等 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 能否购票')
        for train in train_list:
            train_detail = train.split('|')
            if train_detail[3][0] in TRAIN_TYPE:
                print(train_detail[3],
                      trans_city_code(train_detail[6]),
                      trans_city_code(train_detail[7]),
                      train_detail[8],
                      train_detail[9],
                      train_detail[10],
                      check_no(train_detail[32]),
                      check_no(train_detail[31]),
                      check_no(train_detail[30]),
                      check_no(train_detail[21]),
                      check_no(train_detail[23]),
                      check_no(train_detail[33]),
                      check_no(train_detail[24]),
                      check_no(train_detail[28]),
                      check_no(train_detail[29]),
                      check_no(train_detail[26]),
                      train_detail[11])
                print('----------------------------------------------------------------')
        print('----------------------------------------------------------------')
    else:
        print('没有车次')


def choose_seat(seat):
    return SEAT[seat]


def search_ticket():
    i = 0
    print('开始查票...')
    while True:
        time.sleep(TIME_DELAY)
        i += 1
        print('第%d次查询' % i)
        response = session.get(URLINFO['url_query'].format(
            train_date=TRAIN_DATE,
            from_station_code=FROM_STATION_CODE,
            to_station_code=TO_STATION_CODE))
        train_list = response.json()['data']['result']
        for train in train_list:
            train_detail = train.split('|')
            if train_detail[3] in TRAIN_WANTED:
                print(train_detail[3],
                      trans_city_code(train_detail[6]),
                      trans_city_code(train_detail[7]),
                      train_detail[8],
                      train_detail[9],
                      train_detail[10],
                      check_no(train_detail[32]),
                      check_no(train_detail[31]),
                      check_no(train_detail[30]),
                      check_no(train_detail[21]),
                      check_no(train_detail[23]),
                      check_no(train_detail[33]),
                      check_no(train_detail[24]),
                      check_no(train_detail[28]),
                      check_no(train_detail[29]),
                      check_no(train_detail[26]),
                      train_detail[11])
                print('----------------------------------------------------------------')

                for seat in SEAT_WANTED:
                    if train_detail[int(seat)] != '无' or train_detail[int(seat)] != '' and train_detail[11] == 'Y':
                        print('查到车次')
                        return(train_detail[0],
                               trans_city_code(train_detail[6]),
                               trans_city_code(train_detail[7]),
                               choose_seat(seat))



def find_tickets():
    if FROM_STATION_CODE and TO_STATION_CODE:
        i = 3
        while i:
            try:
                response = session.get(URLINFO['url_query'].format(
                    train_date=TRAIN_DATE,
                    from_station_code=FROM_STATION_CODE,
                    to_station_code=TO_STATION_CODE),
                    headers=HEADERS
                )
                train_list = response.json()['data']['result']
                # print_train_info(train_list)
                return(search_ticket())
            except Exception as e:
                print(e)
                time.sleep(1)
                i -= 1

    else:
        print('城市不存在')
    print('Done')


def choose_passenger(info):
    passengers = info['data']['normal_passengers']
    for passenger in passengers:
        if passenger['passenger_name'] == PASSENGER:
            passenger_detail = {
                'passenger_flag': passenger['passenger_flag'],
                'passenger_type': passenger['passenger_type'],
                'passenger_name': passenger['passenger_name'],
                'passenger_id_type_code': passenger['passenger_id_type_code'],
                'passenger_id_no': passenger['passenger_id_no'],
                'mobile_no': passenger['mobile_no']
            }
            return passenger_detail
    return False


def book_ticket(train_secret_str, from_station, to_station, seat):
    # 1 subOrderRequest
    print('subOrderRequest...')
    data = {
        'secretStr': train_secret_str,
        'train_date': TRAIN_DATE,
        'back_train_date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
        'tour_flag': 'dc',
        'purpose_code': 'ADULT',
        'query_from_station_name': from_station,
        'query_to_station_name': to_station,
        'undefined': ''
    }
    data = str(data)[1:-1].replace(':', '=').replace(',', '&').replace(' ', '').replace('\'', '')
    data = requests.utils.requote_uri(data)
    response = session.post(URLINFO['submitOrderRequest']['url'],
                            headers=URLINFO['submitOrderRequest']['headers'],
                            data=data).json()
    # print(response)
    if response['status']:
        print('subOrderRequest Succeed')
    else:
        print('subOrderRequest Failed')
        print(response['messages'])
        sys.exit()

    # 2 initDC
    print('init')
    try:
        response = session.post(URLINFO['initDC']['url'],
                                headers=URLINFO['initDC']['headers'],
                                data='_json_att=')
    except:
        sys.exit()
    pattern = re.compile('globalRepeatSubmitToken = \'(.*?)\'')
    pattern2 = re.compile('ticketInfoForPassengerForm=(.*?);')
    globalRepeatSubmitToken = pattern.findall(response.text)[0]
    ticketInfoForPassengerForm = json.loads(pattern2.findall(response.text)[0].replace('\'', '\"'))
    # print(globalRepeatSubmitToken)
    # print(ticketInfoForPassengerForm)

    # 3 getPassengerDTOs
    print('getPassengerMessage...')
    data = {
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': globalRepeatSubmitToken,
    }
    try:
        response = session.post(URLINFO['passenger']['url'],
                                headers=URLINFO['passenger']['headers'],
                                data=data).json()
        # print(response)
        passenger = choose_passenger(response)
        # print('get ' + passenger['passenger_name'] + '\'s message ')
    except Exception as e:
        print(e)
        sys.exit()

    # 4 checkOrderInfo
    print('checkOrderInfo...')
    passengerTicketStr = seat + ',' + \
                         passenger['passenger_flag'] + ',' + \
                         passenger['passenger_type'] + ',' + \
                         passenger['passenger_name'] + ',' + \
                         passenger['passenger_id_type_code'] + ',' + \
                         passenger['passenger_id_no'] + ',' + \
                         passenger['mobile_no'] + ',N'
    oldPassengerStr = passenger['passenger_name'] + ',' + \
                      passenger['passenger_id_type_code'] + ',' + \
                      passenger['passenger_id_no'] + ',' + \
                      passenger['passenger_type'] + '_'

    data = 'cancel_flag=2&bed_level_order_num=000000000000000000000000000000&passengerTicketStr={}&oldPassengerStr={}_&tour_flag=dc&randCode=&whatsSelect=1&_json_att=&REPEAT_SUBMIT_TOKEN={}'.format(
        passengerTicketStr, oldPassengerStr, globalRepeatSubmitToken)
    data = requests.utils.requote_uri(data)
    response = session.post(URLINFO['checkOrderInfo']['url'],
                            headers=URLINFO['checkOrderInfo']['headers'],
                            data=data).json()
    # print(response)
    if response['data']['submitStatus']:
        print('checkOrderInfo Succeed')
    else:
        print('checkOrderInfo Failed')
        print(response)
        sys.exit()

    # 5 getQueueCount
    print('getQueueCount...')
    date_GMT = time.strftime('%a %b %d %Y %H:%M:%S  GMT+0800', time.strptime(TRAIN_DATE, '%Y-%m-%d'))
    data = {
        'train_date': date_GMT,
        'train_no': ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_no'],
        'stationTrainCode': ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['station_train_code'],
        'seatType': seat,
        'fromStationTelecode': ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['from_station'],
        'toStationTelecode': ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['to_station'],
        'leftTicket': ticketInfoForPassengerForm['leftTicketStr'],
        'purpose_codes': '00',
        'train_location': ticketInfoForPassengerForm['train_location'],
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': globalRepeatSubmitToken,

    }
    response = session.post(URLINFO['getQueueCount']['url'],
                            headers=URLINFO['getQueueCount']['headers'],
                            data=data).json()
    if response['status']:
        print('getQueueCount Succeed')
    else:
        print('getQueueCount Failed')
        print(response)
        sys.exit()

    # 6 confirmSingleForQueue
    print('confirmSingleForQueue...')
    data = {
        'passengerTicketStr': passengerTicketStr,
        'oldPassengerStr': oldPassengerStr,
        'randCode': '',
        'purpose_codes': '00',
        'key_check_isChange': ticketInfoForPassengerForm['key_check_isChange'],
        'leftTicketStr': ticketInfoForPassengerForm['leftTicketStr'],
        'train_location': ticketInfoForPassengerForm['train_location'],
        'choose_seats': '',
        'seatDetailType': '000',
        'whatsSelect': '1',
        'roomType': '00',
        'dwAll': 'N',
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': globalRepeatSubmitToken,
    }
    i = 3
    while i:
        try:
            response = session.post(URLINFO['confirmSingleForQueue']['url'],
                                    headers=URLINFO['confirmSingleForQueue']['headers'],
                                    data=data).json()
        # print(response)
            if response['data']['submitStatus']:
                print('confirmSingleForQueue Succeed')
                break
            else:
                print('confirmSingleForQueue Failed')
                print(response['data']['errMsg'])
                # sys.exit()
        except Exception as e:
            print(e)
            # sys.exit()
        time.sleep(2)
        i -= 1
        if i == 0:
            sys.exit()

    # 7 queryOrderWaitTime
    print('queryOrderWaitTime...')
    i = 20
    while i:
        try:
            response = session.get(URLINFO['queryOrderWaitTime']['url'].format(
                round(time.time()*1000), globalRepeatSubmitToken),
                headers=URLINFO['queryOrderWaitTime']['headers'])
            if response.json()['data']['waitTime'] == -1:
                order_id = response.json()['data']['orderId']
                # print(orderId)
                break
        except Exception as e:
            print(e)
            print('queryOrderWaitTime error')
            i -= 1
        time.sleep(1)
        if i == 0:
            sys.exit()

    # 8 resultOrderForDcQueue
    print('resultOrderForDcQueue...')
    data = 'orderSequence_no={}&_json_att=&REPEAT_SUBMIT_TOKEN={}'.format(order_id, globalRepeatSubmitToken)
    # print(data)
    response = session.post(URLINFO['resultOrderForDcQueue']['url'],
                            headers=URLINFO['resultOrderForDcQueue']['headers'],
                            data=data).json()
    # print(response)
    print('')
    try:
        if response['data']['submitStatus']:
            print('订票成功，请登录12306查看')
        else:
            print(response['data']['errMsg'])
            print('订票失败')
    except Exception as e:
        print(e)


def main():
    if login():
        train_secret_str, from_station, to_station, seat = find_tickets()
        book_ticket(train_secret_str, from_station, to_station, seat)

    print('Done')


if __name__ == '__main__':
    main()

