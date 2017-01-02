from __future__ import print_function
import sys
from utils import Options, RouterApi, generate_table, ArgumentException

def run_program():
    opts = Options(sys.argv[1:])
    apidir = opts.get_or_fail('apidir')
    sys.path.append(apidir)
    hostname = opts.get_or_fail('hostname')
    username = opts.get_or_fail('username')
    password = opts.get_or_fail('password')
    port = opts.get_int_or_default('port', 8728)
    api = RouterApi(hostname, username, password, port)
    command = opts.get_or_fail('command')
    if command == 'dhcp':
        leases = api.get_leases()
        table = generate_table(leases, {
            'status': 'Status',
            'comment': 'Comment',
            'mac-address': 'MAC Address',
            'host-name': 'Hostname',
            'address': 'IP Address',
            'last-seen': 'Last Seen',
            'expires-after': 'Expires'
        })
        print(table)
    else:
        raise ArgumentException('Unknown command %s' % command)


try:
    run_program()
except ArgumentException as e:
    print("Invocation error: %s" % (e.message), file=sys.stderr)
    sys.exit(1)

