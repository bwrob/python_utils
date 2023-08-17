import os
import glob
import time
import pyautogui

user = 'bw200'
path_dict = {
    'powershell': 'C:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe',
    'onenote': 'C:\\',
    'temp_path': 'C:\\temp\\'
}


def start_process(name, delay=5):
    pyautogui.hotkey('winleft', 'd')
    run_path = path_dict.get(name, None)
    if run_path is not None:
        os.startfile(run_path)
        time.sleep(delay)


def folder_path_files(path):
    def filter_files(file_paths, excludes):
        for exclude in excludes:
            file_paths = [file for file in file_paths if exclude not in os.path.basename(file)]
        return file_paths

    file_format = path.strip('\\') + '\\*'
    files = filter_files(glob.glob(file_format), ['$', 'tmp'])
    return list(zip(files, [5] * len(files)))


if __name__ == '__name__':
    processes = ['powershell']
    processes += folder_path_files('temp_path')

    for process in processes:
        start_process(*process)
