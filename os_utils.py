import os
import subprocess


def create_folder(folder_name):
    subprocess.run(["mkdir", folder_name], capture_output=True, text=True)


def create_folder_if_not_exists(folder_path):
    if check_if_exists(folder_path) is False:
        create_folder(folder_path)


def create_file(file_name, path):
    subprocess.run(["touch", file_name], capture_output=True, text=True, cwd=path)


def remove_folder(folder_name):
    subprocess.run(["rm", "-rf", folder_name], capture_output=True, text=True)


def check_if_exists(name):
    if os.path.exists(name):
        return True
    else:
        return False
