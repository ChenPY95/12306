# -*-coding:utf-8-*-
from train import trans_city_code


# 用户名
USER_NAME = ''
# 密码
PASSWORD = ''
# 乘车人
PASSENGER = ''

# 乘车日期
TRAIN_DATE = '2018-05-18'
# 出发站
FROM_STATION = '杭州'
FROM_STATION_CODE = trans_city_code(FROM_STATION)
# 到达站
TO_STATION = '上海'
TO_STATION_CODE = trans_city_code(TO_STATION)
# 查看火车类型  G:高铁  D:动车  Z:直达  T:特快  K:快
TRAIN_TYPE = 'G'
# 抢票车次
TRAIN_WANTED = ['G1520', 'G1384']
# 选择座位  32:特等座 31:一等座 30:二等座 21:高级软卧 23:软卧 33:动卧 24:硬卧 28:软座 29:硬座 26:无座
# 有优先级
SEAT_WANTED = ['30']
# 刷票时间
TIME_DELAY = 3


