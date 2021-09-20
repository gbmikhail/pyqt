# 1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения («Узел
# доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
from ipaddress import ip_address, IPv4Address
from subprocess import Popen, PIPE

import chardet as chardet


# def host_ping(hosts):
#     for ip in hosts:
#         name = ip.exploded if isinstance(ip, IPv4Address) else ip
#         args = ["ping", name]
#         process = Popen(args, stdout=PIPE)
#
#         data = process.communicate()
#         result = chardet.detect(data[0])
#         out = data[0].decode(result['encoding'])
#         if out.find('Заданный узел недоступен') > 0:
#             print(name, '- Узел недоступен')
#         else:
#             print(name, '- Узел доступен')
#
#
# if __name__ == '__main__':
#     host_list = [ip_address(f'192.168.0.{x}') for x in range(1, 11)]
#     host_list.append('yandex.ru')
#
#     host_ping(host_list)


def host_ping(hosts):
    for ip in hosts:
        name = ip.exploded if isinstance(ip, IPv4Address) else ip
        args = ["ping", name]
        process = Popen(args, stdout=PIPE)

        data = process.communicate()
        result = chardet.detect(data[0])
        out = data[0].decode(result['encoding'])
        yield name, 'Узел недоступен' if out.find('Заданный узел недоступен') > 0 else 'Узел доступен'


if __name__ == '__main__':
    host_list = [ip_address(f'192.168.0.{x}') for x in range(1, 11)]
    host_list.append('yandex.ru')

    for name, state in host_ping(host_list):
        print(name, '-', state)
