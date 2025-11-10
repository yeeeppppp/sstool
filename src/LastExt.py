def main():
     print("Функция выполняется...")
import os
import glob
import csv
from datetime import datetime, timedelta

output_dir = 'C:/output'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'recent_access_files.csv')

time_threshold = datetime.now() - timedelta(days=1)

extensions = ['*.py', '*.bat', '*.exe']

excluded_dirs = [
    os.path.normpath(r'C:\Windows\System32'),
    os.path.normpath(r'C:\Windows\SysWOW64'),
    os.path.normpath(r'C:\Windows\WinSxS')
]
def is_in_excluded_dirs(file_path):
    file_path_norm = os.path.normpath(file_path)
    for excl_dir in excluded_dirs:
        if file_path_norm.startswith(excl_dir):
            return True
    return False

search_path = 'C:/'

recent_files = []

for ext in extensions:
    for file_path in glob.glob(os.path.join(search_path, '**', ext), recursive=True):
        try:
            if is_in_excluded_dirs(file_path):
                continue

            access_time = os.path.getatime(file_path)
            access_datetime = datetime.fromtimestamp(access_time)
            if access_datetime >= time_threshold:
                recent_files.append({
                    'path': file_path,
                    'last_accessed': access_datetime.strftime('%Y-%m-%d %H:%M:%S')
                })
        except OSError:
            pass

with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['File Path', 'Last Accessed'])
    writer.writeheader()
    for file_info in recent_files:
        writer.writerow({'File Path': file_info['path'], 'Last Accessed': file_info['last_accessed']})

print(f'Последние открытые файлы за последние сутки, исключая системные папки, сохранены в: {output_path}')

