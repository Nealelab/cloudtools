from subprocess import call

def init_parser(parser):
    parser.add_argument('name', type=str, help='Cluster name.')
    parser.add_argument('--zone', '-z', default='us-central1-b',
                        help='Compute zone for the cluster (default: %(default)s).')
    parser.add_argument('--elk', action='store_true',
                        help='Stop an ELK vm.')
    parser.add_argument('--all', action='store_true',
                        help='Stop both cluster and ELK vm.')

def main(args):
    if args.elk or args.all:
        name = args.name + "-elk"
        print("Stopping virtual machine '{}'...".format(name))
        call(['gcloud', 'compute', 'instances', 'delete', '--quiet', '--zone={}'.format(args.zone), name])
        
    if not args.elk or args.all:
        print("Stopping cluster '{}'...".format(args.name))
        call(['gcloud', 'dataproc', 'clusters', 'delete', '--quiet', args.name])
