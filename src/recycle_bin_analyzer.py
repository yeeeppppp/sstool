def main():
     print("Функция выполняется...")
import os
import datetime
import string
import ctypes
import subprocess
import csv
FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_SYSTEM = 0x4

def get_logical_drives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def get_folder_modification_time(folder_path):
    try:
        mtime = os.path.getmtime(folder_path)
        return datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "Недоступна"

def get_file_attributes(path):
    attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
    if attrs == -1:
        raise ctypes.WinError()
    return attrs

def is_hidden_or_system(attrs):
    return bool(attrs & FILE_ATTRIBUTE_HIDDEN or attrs & FILE_ATTRIBUTE_SYSTEM)

def find_recycle_bin_on_drive(drive):
    recycle_path = os.path.join(drive, "$Recycle.Bin")
    bins_found = []
    if os.path.exists(recycle_path):
        try:
            for entry in os.scandir(recycle_path):
                if entry.is_dir(follow_symlinks=False):
                    try:
                        attrs = get_file_attributes(entry.path)
                        bins_found.append(entry.path)
                    except Exception:
                        bins_found.append(entry.path)
        except Exception:
            pass
    return bins_found

def get_ultimo_ochistku_koznina():
    results = []
    for drive in get_logical_drives():
        recycle_bins = find_recycle_bin_on_drive(drive)
        if recycle_bins:
            last_dates = []
            for bin_path in recycle_bins:
                date_str = get_folder_modification_time(bin_path)
                if date_str != "Недоступна":
                    try:
                        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        last_dates.append(dt)
                    except Exception:
                        pass
            if last_dates:
                last_date = max(last_dates).strftime('%Y-%m-%d %H:%M:%S')
            else:
                last_date = "N/A"
            results.append({
                'drive': drive,
                'recycle_paths': recycle_bins,
                'last_clean_date': last_date
            })
        else:
            results.append({
                'drive': drive,
                'recycle_paths': 'Не найдена',
                'last_clean_date': 'N/A'
            })
    return results

def get_current_user_sid():
    command = 'powershell -Command "[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value"'
    sid = subprocess.check_output(command, shell=True).decode().strip()
    return sid

def get_files_in_recycle_bin(recycle_path):
    """Собирает все файлы внутри папки корзины."""
    if not os.path.exists(recycle_path):
        print(f"Папка по пути {recycle_path} не найдена.")
        return []

    files_data = []
    for root, dirs, files in os.walk(recycle_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                stat = os.stat(file_path)
                ctime = datetime.datetime.fromtimestamp(stat.st_ctime)
                mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
                files_data.append({
                    'file_name': filename,
                    'full_path': file_path,
                    'created_time': ctime.strftime('%Y-%m-%d %H:%M:%S'),
                    'modified_time': mtime.strftime('%Y-%m-%d %H:%M:%S')
                })
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")
    return files_data

def save_to_csv(data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file_name', 'full_path', 'created_time', 'modified_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    user_sid = get_current_user_sid()
    recycle_path = fr"C:\$Recycle.Bin\{user_sid}"
    files = get_files_in_recycle_bin(recycle_path)
    output_csv_path = r"C:\output\trash.csv"
    save_to_csv(files, output_csv_path)
    print(f"Данные корзины пользователя успешно сохранены в {output_csv_path}")
    print("\nДаты последней очистки корзины на всех дисках:")
    cleanup_info = get_ultimo_ochistku_koznina()
    for info in cleanup_info:
        print(f"Диск: {info['drive']}")
        print(f"Путь(и): {info['recycle_paths']}")
        print(f"Дата последней очистки: {info['last_clean_date']}")
        print("-" * 50)

if __name__ == "__main__":
    main()