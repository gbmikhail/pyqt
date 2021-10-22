# 2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только последний
# октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.
from ipaddress import ip_address

from task_1 import host_ping


def host_range_ping(network, begin, end):
    return [network + x for x in range(begin, end + 1)]


if __name__ == '__main__':
    network = ip_address('192.168.0.0')
    host_list = host_range_ping(network, 5, 10)

    for name, state in host_ping(host_list):
        print(name, '-', state)

