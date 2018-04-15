# -*-coding:utf-8-*-

URLINFO = {
    'url_query': 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_station_code}&leftTicketDTO.to_station={to_station_code}&purpose_codes=ADULT',

    'init': {
        'url': 'https://kyfw.12306.cn/otn/login/init',
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
        },
    },

    'captcha-image': {
        'url': 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{}',
    },

    'captcha-check': {
        'url': 'https://kyfw.12306.cn/passport/captcha/captcha-check',
        'headers': {
            'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': r'https://kyfw.12306.cn/otn/login/init',
        }
    },

    'login': {
        'url': 'https://kyfw.12306.cn/passport/web/login',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
        },
    },

    'userLogin': {
        'url': 'https://kyfw.12306.cn/otn/login/userLogin',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
        },
    },

    'userLoginRedirect': {
        'url': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
    },

    'uamtk': {
        'url': 'https://kyfw.12306.cn/passport/web/auth/uamtk',
        'headers': {
            'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
        }
    },

    'uamauthclient': {
        'url': 'https://kyfw.12306.cn/otn/uamauthclient',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
        }
    },

    'city_code': {
        'url': 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9050',
    },

    'checkUser': {
        'url': 'https://kyfw.12306.cn/otn/login/checkUser',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
        }
    },

    'loginOut': {
        'url': 'https://kyfw.12306.cn/otn/login/loginOut',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/index/initMy12306'
        }
    },

    'submitOrderRequest': {
        'url': 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
        }
    },

    'initDC': {
        'url': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'
        }
    },

    'passenger': {
        'url': 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/confirePassenger/initDc',
        }
    },

    'checkOrderInfo': {
        'url': 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
        'data': 'cancel_flag=2&bed_level_order_num=000000000000000000000000000000&passengerTicketStr={}&oldPassengerStr={}_&tour_flag=dc&randCode=&whatsSelect=1&_json_att=&REPEAT_SUBMIT_TOKEN={}',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
    },

    'getQueueCount': {
        'url': 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
    },

    'confirmSingleForQueue': {
        'url': 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingle',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
    },

    'queryOrderWaitTime':  {
        'url': 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
    },

    'resultOrderForDcQueue': {
        'url': 'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        }
    },

}

HEADERS = {
    'Origin': 'https://kyfw.12306.cn',
    'Host': 'kyfw.12306.cn',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': r'https://kyfw.12306.cn/otn/login/init'

}


# 特等座(32),一等座(31),二等座(30),高级软卧(21),软卧(23),动卧(33),硬卧(24),软座(28),硬座(29)无座(26)
# 商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)
SEAT = {
    '32': '9',
    '31': 'M',
    '30': 'O',
    '21': '6',
    '23': '4',
    '24': '3',
    '28': '2',
    '29': '1',
    '26': '1',
}
