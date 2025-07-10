import logging
import os
import platform


def get_drive_path():
    if platform.system() == 'Darwin':
        log_root = "/Volumes/GoogleDrive/My Drive/PLICO_CLOUD/ADMIN/automation_logging"
    elif platform.system() == 'Windows':
        log_root = r'G:\My Drive\PLICO_CLOUD\ADMIN\automation_logging'
    elif platform.system() == 'Linux':
        log_root = 'path to linux log folder on gd'
    else:
        log_root = None
    return log_root


def generate_log_file_name():
    full_path = __file__
    file_name_and_ext = os.path.basename(full_path)
    file_name, _ = os.path.splitext(file_name_and_ext)
    log_file_name = file_name + '_log.log'
    return log_file_name


def setup_logging():

    log_root = get_drive_path()
    if log_root:
        log_file_name = generate_log_file_name()
        filename = os.path.join(log_root, log_file_name)
        with open(filename, 'w') as f:
            pass
        filepath = os.path.join(log_root, filename)
        logging.basicConfig(filename=filepath, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(message, level=logging.INFO):
    if level == logging.INFO:
        logging.info(message)
    elif log_message == logging.ERROR:
        logging.error(message, exc_info=True)


