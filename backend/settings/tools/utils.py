import os


def create_directories(*args):
    """
    Create logs directories
    :param args: list of directories path
    :return: None
    """
    for dir_path in args:
        try:
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
        except OSError:
            pass
