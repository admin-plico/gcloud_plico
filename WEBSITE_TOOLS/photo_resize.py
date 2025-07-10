import json
import os
import sys
import re
import shutil
import subprocess
import platform

requirements_file = 'requirements.txt'
try:
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', requirements_file],
                            capture_output=True, text=True)
except FileNotFoundError as e:
    print(f'error:{e}')

from PIL import Image
from pdf2image import convert_from_path
from photo_resize_db import instantiate_image_tables,  get_last_id, set_last_id

num_pat = r"(\d*)-(.*)\..*$"
old_web_pat = r'.*(WEB)-\d\..*$'
new_web_pat = r'.*_(WEB)'
DATELESS_CONTAINER_PAT = r'\d{6} (.*)'

NO_SERIAL_FN = R'\d*-(.*)\..*'
CURRENT_PROCESSED_PAT = R"(\d{6}) (.*)-\d*-(.*)_WEB\..*"
cwd = os.getcwd()
instantiate_image_tables()


def sort_new_additional_files(input_path):
    # processed = list_processed(input_path)
    files_dict = {}
    for root, dirs, files in os.walk(input_path):
        processed = (os.path.basename(root) == "processed")
        marketing = (os.path.basename(root) == "Marketing")



        if not (processed or marketing):
            for file in files:
                name, extension = os.path.splitext(file)
                # try:

                if extension.lower() in ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'):
                    old_web_found = re.search(old_web_pat, file)
                    new_web_found = re.search(new_web_pat, file)
                    if (old_web_found is None) and (new_web_found is None):
                        # basename, extension = os.path.splitext(file)
                        num_found = re.search(num_pat, file)

                        if num_found:
                            num = num_found.group(1)
                            name = num_found.group(2)
                            if len(num) < 2:
                                num = f"0{num}"
                            temp_name = f"{num}__{name}"
                            entry = {temp_name: os.path.join(root, file)}
                            files_dict.update(entry)

    # print(json.dumps(dict(sorted(files_dict.items())), indent=4))
    return dict(sorted(files_dict.items()))


def list_processed(input_path):

    processed_files = []
    for root, dirs, files in os.walk(input_path):
        processed = (os.path.basename(root) == "processed")
        if processed:
            p_files = os.listdir(root)
            for pf in p_files:
                processed_files.append(pf)
    return processed_files


def resize_and_adjust_image(input_path):
    max_long_side = 2816

    resolution = (144, 144)

    files = sort_new_additional_files(input_path)
    for file_sequence, file_path in files.items():
        try:
            new_file_path = process_image(file_path, max_long_side, resolution)
            new_file_name = os.path.basename(new_file_path)
            marketing_name = new_file_name.replace("WEB", "MARKETING")
            move_originals(file_path, marketing_name)

        except Exception as e:
            print(f'An Error has Occurred: {e}')


def move_originals(file_path, marketing_name):
    file_name = os.path.basename(file_path)
    processed_root = os.path.join(os.path.dirname(file_path), 'processed')
    marketing_root = os.path.join(os.path.dirname(file_path), 'Marketing')
    processed_path = os.path.join(processed_root, file_name)
    marketing_path = os.path.join(marketing_root, marketing_name)
    if not os.path.exists(processed_root):
        os.makedirs(processed_root)
    if not os.path.exists(marketing_root):
        os.makedirs(marketing_root)
    shutil.copy(str(file_path), str(processed_path))
    shutil.move(str(file_path), str(marketing_path))


def process_image(file_path, max_long_side, resolution):

    name = os.path.basename(file_path)
    num_found = re.search(num_pat, name)
    file_name, file_ext = os.path.splitext(name)
    if num_found:
        num = num_found.group(1)
        file_name = num_found.group(2)
    else:
        num = None

    root = os.path.dirname(file_path)
    containing_folder = os.path.basename(root)

    next_id = int(get_last_id(containing_folder)) + 1

    if num:

        if int(num) > next_id:
            serial = num
        else:
            serial = next_id
    else:
        serial = next_id
    if len(str(serial)) < 2:
        serial = f"0{serial}"
    cf_name = re.search(DATELESS_CONTAINER_PAT, containing_folder)
    fn_no_serial = re.search(NO_SERIAL_FN, name)
    pr_file = re.search(CURRENT_PROCESSED_PAT, name)
    new_file_name = f'{containing_folder}-{serial}-{file_name}_WEB{file_ext}'
    if cf_name and fn_no_serial:
        if fn_no_serial.group(1) == cf_name.group(1):

            new_file_name = f'{containing_folder}-{serial}_WEB{file_ext}'

    output_image_path = os.path.join(root, new_file_name)

    with Image.open(file_path) as img:
        long_side = max(img.width, img.height)
        img.info['dpi'] = resolution
        ratio = max_long_side / long_side
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

        img.save(output_image_path)
        set_last_id(containing_folder, serial)
    print(f'processed "{file_name}" to "{new_file_name}"')
    return output_image_path


def test_function():
    test_path = r"C:\Users\dlaqu\OneDrive\Desktop\Website Content"
    resize_and_adjust_image(test_path)


system = platform.system()
folders = ['News Content', 'Projects Content']
dir_paths = []
user = os.getlogin()
if system == "Windows":
    directory = r'G:\My Drive\PLICO_CLOUD\ADMIN\BUSINESS\Web\Website Content'
    if not os.path.exists(directory):
        directory = r'G:\PLICO_CLOUD\ADMIN\BUSINESS\Web\Website Content'
else:
    if user == 'davidlaquerre':
        directory = '/Volumes/GoogleDrive/My Drive/PLICO_CLOUD/ADMIN/BUSINESS/Web/Website Content'
    else:
        directory = f'/Users/{user}/Library/CloudStorage/GoogleDrive-cloud@plicodesignstudio.com/My Drive/PLICO_CLOUD/ADMIN/BUSINESS/Web/Website Content'
for f in folders:
    p = os.path.join(directory, f)
    dir_paths.append(p)

for path in dir_paths:
    resize_and_adjust_image(path)
# # resize_and_adjust_image(cwd)
# test_function()
