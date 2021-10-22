# 3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
# Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
# (использовать модуль tabulate). Таблица должна состоять из двух колонок
from ipaddress import ip_address

from tabulate import tabulate

from task_1 import host_ping
from task_2 import host_range_ping


def host_range_ping_tab(network, begin, end):
    host_list = host_range_ping(network, begin, end)

    ts = []
    for name, state in host_ping(host_list):
        ts.append((name, state))
    print(tabulate(ts))


if __name__ == '__main__':
    network = ip_address('192.168.0.0')
    host_range_ping_tab(network, 5, 10)
