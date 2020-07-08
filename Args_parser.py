import argparse
import json

def args_parser():
	parser = argparse.ArgumentParser(description='Python Plate Scanner')

	parser.add_argument('-d', '--database', action="store", default="plate",
						help="DataBase Name default is [plate]")
	parser.add_argument('-o','--output', action="store", default=None,
						help="Output file name. If not given, default output is: [STDOUT]")
	parser.add_argument('-l', '--log', type=int, default=1,
						help="Log level [0-basic, 1-standard[default], 2-verbose]")
	parser.add_argument('-i', '--input', action="store", default=None,
						help="Input directory name")
	parser.add_argument('-c', '--config', action="store", default=None,
					   help="Configuration file in json format")

	args = parser.parse_args()

	# Read config file if it was provided
	if args.config is not None:
		try:
			config_data=open(args.config,'r')
			config = json.load(config_data)
			config_data.close()
		except Exception as e:
			print(f"Config file: ['{args.config}'] couldn't be opened, please check the file exists.")
			config = {}
	else:
		config = {}

	# Adjust configuration be users given flag parameters
	dict_arg = args.__dict__
	for arg in config:
		if arg in dict_arg:
			if dict_arg[arg] is not None:
				continue
			else:
				dict_arg[arg] = config[arg]
	del(dict_arg['config'])

	if dict_arg["input"] == "" or dict_arg["input"] is None:
		print ("Error: Input directory wasn't provided. Exiting...")
		exit()

	return dict_arg
