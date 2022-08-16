import dis

from pprint import pprint


class ServerVerifier(type):
    def __init__(cls, clsname, bases, clsdict):
        methods_global = []  # 'LOAD_GLOBAL'
        methods_func = []  # 'LOAD_METHOD'
        attributes = []  # 'LOAD_ATTR'
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    print(i)
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods_global:
                            methods_global.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in methods_func:
                            methods_func.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attributes:
                            attributes.append(i.argval)
        # print(20 * '-', 'methods_global', 20 * '-')
        # pprint(methods_global)
        # print(20 * '-', 'methods_func', 20 * '-')
        # pprint(methods_func)
        # print(20 * '-', 'attributes', 20 * '-')
        # pprint(attributes)
        # print(50 * '-')
        if 'connect' in methods_global:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        if not ('SOCK_STREAM' in attributes and 'AF_INET' in attributes):
            raise TypeError('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)


class ClientVerifier(type):
    def __init__(cls, clsname, bases, clsdict):
        client_methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in client_methods:
                            client_methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in client_methods:
                raise TypeError('В классе обнаружено использование запрещённого метода')
            if 'get_message' in client_methods or 'send_message' in client_methods:
                pass
            else:
                raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
            super().__init__(clsname, bases, clsdict)
