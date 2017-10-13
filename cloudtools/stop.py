from subprocess import call

def init_parser(parser):
    parser.add_argument('name', type=str, help='Cluster name.')
    parser.add_argument('--zone', '-z', default='us-central1-b',
                        help='Compute zone for the cluster (default: %(default)s).')
    parser.add_argument('--elk', action='store_true',
                        help='Stop an ELK vm.')

def main(args):
    if args.elk:
        name = args.name + "-elk"
        print("Stopping virtual machine '{}'...".format(name))
        call(['gcloud', 'compute', 'instances', 'delete', '--quiet', '--zone={}'.format(args.zone), name])
    else:
        print("Stopping cluster '{}'...".format(args.name))
        call(['gcloud', 'dataproc', 'clusters', 'delete', '--quiet', args.name])
