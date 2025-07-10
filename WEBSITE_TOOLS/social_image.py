from PIL import Image
import os
import platform
import shutil


def set_path():
    syst = platform.system()
    if syst == 'Windows':
        content_path = r"G:\My Drive\PLICO_CLOUD\ADMIN\BUSINESS\Web\Web Content\Projects Content"
        logo_path = r'G:\My Drive\PLICO_CLOUD\ADMIN\BUSINESS\LOGOS\PLICO LOGOS\PLICO DESIGN STUDIO_grey.jpg'
    else:
        content_path = ''
        logo_path = ''
    paths = [logo_path, content_path]
    return paths


def add_logo(margin=100):
    scale_factor = 0.5
    logo_path, content_path = set_path()
    for root, folder, files in os.walk(content_path):
        for file in files:
            containing_folder = os.path.basename(root)
            if containing_folder.lower() == "social":
                file_name, ext = os.path.splitext(file)
                if file_name[-6:] != 'Social':
                    if ext.lower() in ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'):

                        output_image_path = os.path.join(root, f'{file_name}_social.png')
                        main_image_path = os.path.join(root, file)
                        dest_folder = os.path.join(root, 'processed')

                        if not os.path.exists(dest_folder):
                            os.mkdir(dest_folder)

                        main_image = Image.open(main_image_path).convert("RGBA")
                        logo_image = Image.open(logo_path)
                        new_size = (int(logo_image.width * scale_factor), int(logo_image.height * scale_factor))
                        logo_image = logo_image.resize(new_size, Image.LANCZOS).convert("RGBA")
                        x_position = margin
                        y_position = main_image.height - logo_image.height - margin
                        main_image.paste(logo_image, (x_position, y_position), logo_image)
                        main_image.save(output_image_path)
                        processed_path = os.path.join(dest_folder, file)
                        shutil.move(main_image_path, processed_path)


# Usage example
add_logo()

