
import os
import argparse


parser = argparse.ArgumentParser(description='Ping script')
parser.add_argument('-f', action="store", dest="file")
parser.add_argument('-t', action="store", dest="table")
parser.add_argument('-db', action="store", dest="db")
args = parser.parse_args()


working_dirs = [
    os.path.join(os.environ['USERPROFILE'], 'Desktop'),
    os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Scripts'),
]


# Get file name from -f command line arg
def get_args():
    return args


def find_file(file_name):
    for directory in working_dirs:
        if file_name in os.listdir(directory):
            return os.path.join(directory, file_name)
