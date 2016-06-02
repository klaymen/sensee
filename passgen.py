import argparse
import hashlib

parser = argparse.ArgumentParser(description='Compute hash for password storage')
parser.add_argument('password', metavar='phrase', type=str, nargs=1, help='a password to be hashed')
args = parser.parse_args()
print hashlib.sha224(args.password[0]).hexdigest()
