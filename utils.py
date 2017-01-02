from tabulate import tabulate


class Options(object):
    def __init__(self, args):
        self.opts = {}
        for arg in args:
            if not arg.startswith('--'):
                raise ArgumentException('Arguments be in the form --key=value')
            parts = arg.split('=', 2)
            if len(parts) != 2:
                raise ArgumentException('Arguments be in the form --key=value')
            key = parts[0][2:]
            value = parts[1]
            self.opts[key] = value

    def get_or_fail(self, key):
        if key in self.opts:
            return self.opts[key]
        else:
            raise ArgumentException('Required argument %s was missing' % (key))

    def get_or_default(self, key, default_value):
        if key in self.opts:
            return self.opts[key]
        else:
            return default_value

    def get_int_or_default(self, key, default_value):
        value = self.get_or_default(key, default_value)
        if isinstance(value, str):
            value = int(value)
        return value


class ArgumentException(Exception):
    pass
    # def __init__(self, message):
    #     Exception.__init__(message)


class RouterApi(object):
    def __init__(self, hostname, username, password, port):
        from routeros_api import connect
        self.connection = connect(hostname, username, password, port)

    def get_leases(self, opts={}):
        return self.connection.get_resource('/ip/dhcp-server/lease').get(*opts)


def generate_table(rows, columns):
    col_set = set(columns.keys())
    filtered = [dict([[k, row[k]] for k in row.keys() if k in col_set and k in row]) for row in rows]
    return tabulate(filtered, headers=columns)
