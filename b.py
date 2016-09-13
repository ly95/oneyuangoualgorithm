#!/usr/bin/env python
# coding=utf-8
"""
一元购中奖算法：
    幸运号码 = 100个时间求和 % 总需人数 + 10000001

    100个时间和 ＝ 商品最后一个号码分配完毕时间点前本站全部商品的最后100个参与时间之和 （包含该商品的最后一人次的参与时间）

    已知 幸运号码。
    已知 每次投注时间

    求解，最后一次购买时间能否在前后5秒内满足中奖结果。
"""

from __future__ import print_function
from __future__ import division

import sys
import argparse
import random
from datetime import datetime, timedelta

# 固定基数
BASE_NUMBER = 10000000

def get_args():
    """
    脚本参数
    """
    parser = argparse.ArgumentParser(description="一元购中奖算法")
    parser.add_argument("-l", type=int, default=None, help="幸运号码")
    parser.add_argument("-t", type=int, default=7088, help="本期总需人次")
    return parser.parse_args()

def make_order(created, tickets):
    """
    订单内容
    """
    return {"created": created, "tickets": tickets}

def fake_orders(tickets_total, last_time, size=1):
    """
    伪造订单
    """

    # 号码库存
    tickets_store = range(BASE_NUMBER + 1, BASE_NUMBER + tickets_total + 1)

    orders = []
    for i in range(0, size):

        # 随机购买几次，得到票
        try:
            tickets = random.sample(tickets_store,  random.randint(1, 10))
        except ValueError:
            break

        # 从库中移除该票
        for i in tickets:
            tickets_store.remove(i)

        # 第二个订单与上一个订单间隔10秒至600秒
        add_value = random.randint(10 * 1000000, 600 * 1000000)
        created = last_time + timedelta(microseconds=add_value)
        last_time = created
        orders.append(make_order(created, tickets))
    
    for i in orders:
        print("--------------------")
        print("购买时间", str(i.get('created'))[:-3])
        print("购买号码", i.get("tickets"))
    print("--------------------")
    print("最后%d条订单数据" % len(orders))
    # print(len(tickets_store))

    return orders

def algorithm(luckly_number, total_tickets, time_sum, last_order_time, max_time=None):
    ret = None
    new_time_sum = time_sum + last_order_time
    while True:
        new_time_sum += 1
        if max_time is not None and new_time_sum - time_sum > max_time:
            break
        if (new_time_sum % total_tickets + 1) == luckly_number:
            ret = new_time_sum - time_sum
            break

    return ret

def transform_time(t):
    return int(str(t.strftime("%H%M%S%f"))[:9])

def main():
    args = get_args()
    total_tickets = args.t
    luckly_number = args.l if args.l is not None and args.l < total_tickets else random.randint(1, total_tickets)
    
    orders = fake_orders(total_tickets, datetime.now(), 99)
    print("幸运号码", luckly_number + BASE_NUMBER)

    # 时间和
    time_sum = reduce(lambda x, y: x + y, map(lambda x: transform_time(x.get("created")), orders))
    print("前%d条订单的时间和" % len(orders), time_sum)

    raw_input("\r\n> 购买最后一个号码...")

    now_time = datetime.now()
    current_time = transform_time(now_time)
    print("实际当前时间", str(now_time), "转化后", current_time)

    time = algorithm(luckly_number, total_tickets, time_sum, current_time-4999, current_time+4999)
    print("调整后时间", time)
    print("相差", abs(current_time - time), "毫秒")


if __name__ == "__main__":
    main()
