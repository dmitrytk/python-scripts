import argparse
import os

parser = argparse.ArgumentParser(description='Ping script')
parser.add_argument('-f', action="store", dest="file")
parser.add_argument('-t', action="store", dest="table")
parser.add_argument('-db', action="store", dest="db")
args = parser.parse_args()

working_dirs = [
    os.path.join(os.environ['USERPROFILE'], 'Desktop'),
    os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Scripts'),
]


def get_args():
    """Get file name from -f command line arg"""

    return args


def find_file(file_name):
    """Find file in working_dirs"""

    for directory in working_dirs:
        if file_name in os.listdir(directory):
            return os.path.join(directory, file_name)
