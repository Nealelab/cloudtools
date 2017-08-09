import os
from subprocess import Popen, check_call

def init_parser(parser):
    parser.add_argument('name', type=str, help='Cluster name.')
    parser.add_argument('service', type=str,
                        choices=['r', 'rstudio'],
                        help='Web service to launch.')
    parser.add_argument('--port', '-p', default='10000', type=str,
                        help='Local port to use for SSH tunnel to master node (default: %(default)s).')
    parser.add_argument('--zone', '-z', default='us-central1-b', type=str,
                        help='Compute zone for Dataproc cluster (default: %(default)s).')

def main(args):
    print("Connecting to cluster '{}'...".format(args.name))

    # shortcut mapping
    shortcut = {
        'r': 'rstudio'
    }

    service = args.service
    if service in shortcut:
        service = shortcut[service]

    # Dataproc port mapping
    compute_ports = {
        'rstudio': 8787
    }
    connect_port = compute_ports[service]

    # open SSH tunnel to master node
    cmd = [
        'gcloud',
        'compute',
        'ssh',
        '{}'.format(args.name),
        '--zone={}'.format(args.zone),
        '--ssh-flag=-D {}'.format(args.port),
        '--ssh-flag=-N',
        '--ssh-flag=-f',
        '--ssh-flag=-n'
    ]
    with open(os.devnull, 'w') as f:
        check_call(cmd, stdout=f, stderr=f)

    # open Chrome with SOCKS proxy configuration
    cmd = [
        r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        'http://localhost:{}'.format(connect_port),
        '--proxy-server=socks5://localhost:{}'.format(args.port),
        '--host-resolver-rules=MAP * 0.0.0.0 , EXCLUDE localhost',
        '--user-data-dir=/tmp/'
    ]
    with open(os.devnull, 'w') as f:
        Popen(cmd, stdout=f, stderr=f)
