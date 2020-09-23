
import os

working_dirs = [
    os.path.join(os.environ['USERPROFILE'], 'Desktop'),
    os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Scripts'),
]


def work_file(file_name):
    for directory in working_dirs:
        if file_name in os.listdir(directory):
            return os.path.join(directory, file_name)
