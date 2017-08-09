from subprocess import call

def init_parser(parser):
	parser.add_argument('name', type=str, help='Cluster name.')
	parser.add_argument('--zone', default='us-central1-b',
						help='Compute zone for the instance (default: %(default)s).')
	parser.add_argument('--machine-type', '--machine', '-m', default='n1-highmem-8', type=str,
						help='Machine type (default: %(default)s).')
	parser.add_argument('--boot-disk-size', default=200, type=int,
						help='Disk size of machine, in GB (default: %(default)s).')
	parser.add_argument('--image', type=str, 
						help='Name of image to use to start instance.')


def main(args):
	print("Starting instance '{}'...".format(args.name))

	cmd = [
		'gcloud',
		'compute',
		'instances',
		'create',
		args.name,
		'--zone={}'.format(args.zone),
		'--machine-type={}'.format(args.machine_type),
		'--boot-disk-size={}GB'.format(args.boot_disk_size)
	]

	if args.image:
		cmd.append('--image={}'.format(args.image))

	call(cmd)
	