import os
from subprocess import Popen, check_call


def init_parser(parser):
    parser.add_argument('name', type=str, help='Cluster name.')
    parser.add_argument('service', type=str,
                        choices=['notebook', 'nb', 'spark-ui', 'ui', 'spark-ui1', 'ui1',
                                 'spark-ui2', 'ui2', 'spark-history', 'hist', 'elk', 'elk-history'],
                        help='Web service to launch.', nargs='+')
    parser.add_argument('--port', '-p', default='10000', type=str,
                        help='Local port to use for SSH tunnel to master node (default: %(default)s).')
    parser.add_argument('--elk-port', default='10001', type=str,
                        help='Local port to use for SSH tunnel to elk node (default: %(default)s).')
    parser.add_argument('--zone', '-z', default='us-central1-b', type=str,
                        help='Compute zone for Dataproc cluster (default: %(default)s).')

def main(args):
    print("Connecting to cluster '{}'...".format(args.name))

    # shortcut mapping
    shortcut = {
        'ui': 'spark-ui',
        'ui1': 'spark-ui1',
        'ui2': 'spark-ui2',
        'hist': 'spark-history',
        'nb': 'notebook'
    }

    # Dataproc port mapping
    dataproc_ports = {
        'spark-ui': 4040,
        'spark-ui1': 4041,
        'spark-ui2': 4042,
        'spark-history': 18080,
        'notebook': 8123,
        'elk': 5601,
        'elk-history': 18080
    }

    def is_elk(s):
        return s == 'elk' or s == 'elk-history'

    service = [shortcut.get(s, s) for s in args.service]
    inputs = [('{}-elk'.format(args.name), args.elk_port, dataproc_ports[s]) if is_elk(s) else ('{}-m'.format(args.name), args.port, dataproc_ports[s]) for s in service]

    for name, localport, remoteport in inputs:
        # open SSH tunnel
        cmd = [
            'gcloud',
            'compute',
            'ssh',
            '{}'.format(name),
            '--zone={}'.format(args.zone),
            '--ssh-flag=-D {}'.format(localport),
            '--ssh-flag=-N',
            '--ssh-flag=-f',
            '--ssh-flag=-n'
        ]

        with open(os.devnull, 'w') as f:
            check_call(cmd, stdout=f, stderr=f)

        # open Chrome with SOCKS proxy configuration
        cmd = [
            r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            'http://localhost:{}'.format(remoteport),
            '--proxy-server=socks5://localhost:{}'.format(localport),
            '--host-resolver-rules=MAP * 0.0.0.0 , EXCLUDE localhost',
            '--user-data-dir=/tmp/chrome{}'.format(localport)
        ]
        with open(os.devnull, 'w') as f:
            Popen(cmd, stdout=f, stderr=f)
